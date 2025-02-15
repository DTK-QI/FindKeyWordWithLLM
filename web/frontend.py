import streamlit as st
import requests
from annotated_text import annotated_text
from time import sleep

def init_session_state():
    if 'processing' not in st.session_state:
        st.session_state.processing = False
    if 'results' not in st.session_state:
        st.session_state.results = None

# 初始化頁面設置
st.set_page_config(
    page_title="Cancer Report Analysis",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 初始化 session state
init_session_state()

# 自定義 CSS
st.markdown("""
<style>
    .stTextInput > div > div > input {
        min-height: 100px;
    }
    .main {
        padding: 2rem;
    }
    .annotation-result {
        margin: 20px 0;
        padding: 15px;
        border-radius: 5px;
        background-color: #f8f9fa;
    }
    .stAlert {
        padding: 1rem;
        margin-bottom: 1rem;
        border-radius: 0.5rem;
    }
    .keyword-match {
        background-color: #ffd700;
        padding: 0.2rem 0.4rem;
        border-radius: 0.2rem;
    }
    .report-container {
        background-color: #ffffff;
        padding: 2rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# 側邊欄
with st.sidebar:
    st.header("ℹ️ About")
    st.markdown("""
    This tool analyzes medical reports for cancer-related keywords and patterns.
    
    **Features:**
    - Automatic keyword detection
    - Text highlighting
    - Detailed analysis results
    """)
    
    # API 設置
    st.header("⚙️ API Settings")
    api_url = st.text_input(
        "Remote API URL:",
        value="http://192.168.0.202:1234/v1/chat/completions",
        help="Enter the URL of your remote API"
    )
    model_name = st.selectbox(
        "Model:",
        ["llama-3.3-70b-instruct"],
        help="Select the model to use"
    )
    temperature = st.slider(
        "Temperature:",
        min_value=0.0,
        max_value=1.0,
        value=0.85,
        help="Control randomness in the output"
    )
    top_p = st.slider(
        "Top P:",
        min_value=0.0,
        max_value=1.0,
        value=0.3,
        help="Control diversity of the output"
    )
    max_tokens = st.number_input(
        "Max Tokens:",
        min_value=100,
        max_value=4000,
        value=2000,
        help="Maximum number of tokens to generate"
    )

# 主要內容
st.title("🔬 Cancer Report Analysis")
st.markdown("### Input your medical report for analysis")

# 文本輸入
text_input = st.text_area(
    "Enter your medical report:",
    height=200,
    help="Paste your medical report here for analysis",
    placeholder="Enter the medical report text here..."
)

# 進度條容器
progress_container = st.empty()

# 分析按鈕
if st.button("🔍 Analyze Report", type="primary", disabled=st.session_state.processing):
    if text_input:
        try:
            st.session_state.processing = True
            
            # 顯示進度條
            with progress_container:
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # 模擬進度
                for i in range(400):
                    progress_bar.progress(i + 1)
                    status_text.text(f"Analysis in progress... {i+1}%")
                    sleep(0.1)
            
            # 發送請求到 FastAPI search_remote 端點
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
                
                # 清除進度條
                progress_container.empty()
                
                # 顯示結果
                st.markdown("### 📊 Analysis Results")
                
                with st.container():
                    st.markdown("#### Annotated Report")
                    # 準備標註
                    text = text_input
                    annotations = []
                    
                    for result in results:
                        keyword = result["keyword"]
                        match = result["matches"]
                        
                        if match in text:
                            before, after = text.split(match, 1)
                            if before:
                                annotations.append(before)
                            annotations.append((match, f"🔍 {keyword}", "#ffd700"))
                            text = after
                    
                    if text:
                        annotations.append(text)
                    
                    # 在容器中顯示標註的文本
                    with st.expander("View Annotated Text", expanded=True):
                        annotated_text(*annotations)
                
                # 顯示詳細結果
                st.markdown("### 🔍 Detailed Matches")
                for idx, result in enumerate(results):
                    with st.expander(f"Keyword {idx+1}: {result['keyword']}", expanded=True):
                        st.markdown(f"**Match found:**")
                        st.markdown(f"```\n{result['matches']}\n```")
            
            else:
                st.error(f"Error: {response.text}")
        
        except requests.exceptions.RequestException as e:
            st.error(f"Error connecting to the API: {str(e)}")
        
        finally:
            st.session_state.processing = False
            progress_container.empty()
    else:
        st.warning("⚠️ Please enter some text to analyze.")

# 如果有之前的結果，顯示一個重置按鈕
if st.session_state.results:
    if st.button("🔄 Clear Results"):
        st.session_state.results = None
        st.experimental_rerun()