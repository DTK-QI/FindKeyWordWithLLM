import streamlit as st
import requests
from annotated_text import annotated_text
import time

def init_session_state():
    if 'processing' not in st.session_state:
        st.session_state.processing = False
    if 'results' not in st.session_state:
        st.session_state.results = None
    if 'analysis_complete' not in st.session_state:
        st.session_state.analysis_complete = False
    if 'text_input' not in st.session_state:
        st.session_state.text_input = ""

EXAMPLE_TEXT = """The patient presents with a clinical history concerning for suspected cancer recurrence. Recent follow-up imaging with PET-CT has identified multiple new hepatic lesions, raising strong suspicion of liver metastasis originating from previously diagnosed colon cancer. In addition, multiple enlarged lymph nodes have been observed in the pericolonic region, which may indicate lymphatic spread of the malignancy.
Further evaluation of the previous surgical site reveals evidence of local recurrence, with significant invasion into adjacent anatomical structures, suggesting aggressive disease behavior. These findings are consistent with disease progression, demonstrating metastatic involvement in multiple organ systems.
Given the extent of the newly identified lesions and the pattern of dissemination, further oncological assessment is warranted. A multidisciplinary team approach, including oncologists, radiologists, and surgical specialists, will be necessary to determine the best course of action. Potential treatment options may include systemic chemotherapy, targeted therapy, or localized interventions such as radiofrequency ablation for hepatic lesions.
Close monitoring and additional imaging studies, including contrast-enhanced MRI or further PET-CT evaluations, may be required to assess the full extent of metastatic disease. Given the complexity of the case, a reassessment of the patient’s overall prognosis and treatment strategy is crucial to optimize therapeutic outcomes while maintaining the best possible quality of life."""

HELP_TEXT = """
#### 🔍 How to Use:
1. Enter your medical report text in the input box
2. Click 'Load Example' to see a sample cancer recurrence report
3. Adjust model settings in the sidebar if needed
4. Click 'Analyze Report' to detect patterns of cancer recurrence
"""

# CSS and page setup
st.set_page_config(
    page_title="Cancer Report Analysis",
    layout="wide",
    initial_sidebar_state="expanded"
)

init_session_state()

st.markdown("""
<style>
    .stTextInput > div > div > input {
        min-height: 100px;
    }
    .main { padding: 2rem; }
    
    @keyframes spinner {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    .loading-spinner {
        width: 60px;
        height: 60px;
        border: 4px solid rgba(52, 152, 219, 0.1);
        border-left: 4px solid #3498db;
        border-radius: 50%;
        animation: spinner 1s cubic-bezier(0.76, 0.35, 0.2, 0.7) infinite;
        box-shadow: 0 0 15px rgba(52, 152, 219, 0.2);
    }
    
    .loading-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 30px;
        margin: 20px 0;
        background: rgba(255, 255, 255, 0.95);
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        animation: fadeIn 0.5s ease-in-out;
    }
    
    .loading-text {
        margin-top: 20px;
        color: #3498db;
        font-weight: 500;
        font-size: 1.1em;
        text-align: center;
    }
    
    .status-badge {
        padding: 4px 12px;
        border-radius: 15px;
        font-size: 0.9em;
        margin: 5px 0;
        animation: fadeIn 0.3s ease-in-out;
    }
    
    .status-processing {
        background: #e3f2fd;
        color: #1976d2;
        border: 1px solid #bbdefb;
    }
    
    .status-complete {
        background: #e8f5e9;
        color: #2e7d32;
        border: 1px solid #c8e6c9;
    }
    
    .highlight-text {
        background: linear-gradient(120deg, rgb(255, 122, 0) 0%, rgb(255, 122, 0) 100%);
        background-repeat: no-repeat;
        background-size: 100% 0.2em;
        background-position: 0 88%;
        transition: background-size 0.25s ease-in;
        font-weight: 500;
    }
    
    .highlight-text:hover {
        background-size: 100% 88%;
    }
    
    .result-container {
        margin: 15px 0;
        padding: 20px;
        border-radius: 8px;
        background: #5e5e95;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        animation: fadeIn 0.5s ease-in-out;
    }
    
    .match-count {
        font-size: 0.9em;
        color: #666;
        margin-bottom: 10px;
    }
    
    .button-row {
        display: flex;
        gap: 10px;
        margin: 20px 0;
    }
    
    .stButton > button {
        width: 100%;
        padding: 0.5rem 1rem;
        font-weight: 500;
    }
    
    .info-box {
        padding: 1rem;
        background-color: #f8f9fa;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    
    .centered-spinner {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 200px;
    }
    
    .tooltip {
        position: relative;
        display: inline-block;
        border-bottom: 1px dotted #666;
        cursor: help;
    }
    
    .tooltip .tooltiptext {
        visibility: hidden;
        width: 200px;
        background-color: #555;
        color: #fff;
        text-align: center;
        border-radius: 6px;
        padding: 5px;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        margin-left: -100px;
        opacity: 0;
        transition: opacity 0.3s;
    }
    
    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
    
    .help-text {
        background-color: #f8f9fa;
        border-left: 4px solid #4CAF50;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0 0.5rem 0.5rem 0;
    }
    
    .status-message {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
        animation: fadeIn 0.3s ease-in;
    }
    
    .status-message.info {
        background-color: #3a688a;
        border-left: 4px solid #2196f3;
    }
    
    .status-message.success {
        background-color: #5e5e8f;
        border-left: 4px solid #4caf50;
    }
    
    .status-message.warning {
        background-color: #fff3e0;
        border-left: 4px solid #ff9800;
    }
    
    .status-message.error {
        background-color: #52292f;
        border-left: 4px solid #f44336;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ API Settings")
    
    # Help section in sidebar
    with st.expander("ℹ️ Help"):
        st.markdown(HELP_TEXT)
    
    api_url = st.text_input(
        "Remote API URL:",
        value="http://192.168.0.202:1234/v1/chat/completions",
        help="Enter the URL of your LLM API service"
    )
    
    model_name = st.selectbox(
        "Model:",
        ["llama-3.3-70b-instruct"],
        help="Select the model to use for analysis"
    )
    
    with st.expander("Advanced Settings"):
        temperature = st.slider(
            "Temperature:",
            0.0, 1.0, 0.85,
            help="Higher values make the output more random"
        )
        top_p = st.slider(
            "Top P:",
            0.0, 1.0, 0.3,
            help="Controls diversity of the output"
        )
        max_tokens = st.number_input(
            "Max Tokens:",
            100, 4000, 2000,
            help="Maximum number of tokens to generate"
        )

# Main content
st.title("🔬 Cancer Recurrence Analysis")

with st.container():
    st.info(
        "This specialized tool analyzes medical reports to identify patterns of cancer recurrence, "
        "metastatic spread, and disease progression. Enter your report text below or use "
        "the provided example case."
    )

# Text input area
col1, col2 = st.columns([4, 1])
with col1:
    text_input = st.text_area(
        "Enter your oncology report:",
        value=st.session_state.text_input,
        height=200,
        placeholder="Enter the medical report text for cancer recurrence analysis...",
        help="Paste your oncology report text here for analysis of recurrence patterns"
    )
with col2:
    st.markdown("<div style='height: 30px'></div>", unsafe_allow_html=True)  # 添加間距
    if st.button("📝 Load Example", use_container_width=True):
        st.session_state.text_input = EXAMPLE_TEXT
        st.rerun()

# Analysis button
col1, col2, col3 = st.columns([2, 2, 2])
with col2:
    analyze_button = st.button(
        "🔍 Analyze Report",
        type="primary",
        disabled=st.session_state.processing,
        use_container_width=True
    )

# Status containers
loading_container = st.empty()
status_container = st.empty()

# 處理分析按鈕點擊
if analyze_button:
    if text_input:
        try:
            st.session_state.processing = True
            st.session_state.analysis_complete = False
            
            # 顯示加載動畫和狀態
            with loading_container:
                st.markdown("""
                    <div class="loading-container centered-spinner">
                        <div class="loading-spinner"></div>
                        <div class="loading-text">
                            Analyzing medical report...
                            <div class="status-badge status-processing">Processing</div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            # API 請求
            response = requests.post(
                "http://localhost:8080/search_remote",
                json={
                    "report": text_input,
                    "api_url": api_url,
                    "model_name": model_name,
                    "temperature": temperature,
                    "top_p": top_p,
                    "max_tokens": max_tokens
                },
                timeout=180
            )
            
            if response.status_code == 200:
                results = response.json()
                st.session_state.results = results
                st.session_state.analysis_complete = True
                
                # 清除加載動畫
                loading_container.empty()
                
                # 顯示完成狀態
                status_container.markdown("""
                    <div class="status-message success">
                        ✓ Analysis completed successfully
                    </div>
                """, unsafe_allow_html=True)
                
                # 顯示結果
                if not results:
                    st.warning("No matches found in the provided text.")
                else:
                    st.markdown("### 📊 Analysis Results")
                    
                    # 顯示標註文本
                    with st.container():
                        text = text_input
                        annotations = []
                        total_matches = len(results)
                        
                        st.markdown(
                            f"""<div class="status-message info">
                                📌 Found {total_matches} relevant matches in the text
                            </div>""",
                            unsafe_allow_html=True
                        )
                        
                        for result in results:
                            keyword = result.get("keyword", "")
                            match = result.get("matches", "")
                            
                            if match and match in text:
                                parts = text.split(match)
                                if parts[0]:
                                    annotations.append(parts[0])
                                annotations.append((match, f"🔍 {keyword}", "rgb(255, 122, 0)"))  # 改變這裡的顏色
                                text = "".join(parts[1:])
                        
                        if text:
                            annotations.append(text)
                        
                        # 顯示標註
                        with st.expander("📄 View Annotated Report", expanded=True):
                            if annotations:
                                annotated_text(*annotations)
                        
                        # 顯示詳細結果
                        st.markdown("### 🔍 Detailed Findings")
                        for idx, result in enumerate(results, 1):
                            with st.expander(
                                f"""Finding {idx}: {result.get('keyword', '')}""",
                                expanded=False
                            ):
                                st.markdown(
                                    f"""<div class="result-container">
                                        {result.get('matches', 'No match found')}
                                    </div>""",
                                    unsafe_allow_html=True
                                )
            
            else:
                status_container.markdown(
                    f"""<div class="status-message error">
                        ❌ Error: {response.text}
                    </div>""",
                    unsafe_allow_html=True
                )
        
        except requests.exceptions.RequestException as e:
            status_container.markdown(
                f"""<div class="status-message error">
                    ❌ Connection Error: Unable to reach the API server. 
                    Please check your network connection and try again.
                    <br>Error: {str(e)}
                </div>""",
                unsafe_allow_html=True
            )
        
        finally:
            st.session_state.processing = False
            if not st.session_state.analysis_complete:
                loading_container.empty()
    else:
        st.warning("⚠️ Please enter some text to analyze or use the example provided.")

# 重置按鈕
if st.session_state.results or st.session_state.text_input:
    col1, col2, col3 = st.columns([2, 2, 2])
    with col2:
        if st.button("🔄 Clear All", use_container_width=True):
            st.session_state.results = None
            st.session_state.analysis_complete = False
            st.session_state.text_input = ""
            loading_container.empty()
            status_container.empty()
            st.rerun()