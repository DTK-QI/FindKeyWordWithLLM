# Cancer Recurrence Analysis System

This specialized system provides a comprehensive solution for analyzing medical reports to detect and evaluate cancer recurrence patterns using advanced language models.

## Overview

This tool is designed to assist medical professionals in:
- Detecting patterns of cancer recurrence
- Identifying metastatic spread
- Analyzing disease progression
- Evaluating treatment responses
- Monitoring post-surgical outcomes

## Components

### 1. FastAPI Backend
- Specialized API endpoints for cancer recurrence analysis
- Advanced pattern recognition using LLaMA model
- Supports both local and remote processing for complex medical text analysis

### 2. Streamlit Web Interface
- Intuitive interface for oncology report analysis
- Real-time highlighting of recurrence patterns
- Interactive visualization of findings
- Configurable analysis parameters

## Installation

1. Clone the repository:
```bash
$ git clone <repository_url>
$ cd <repository_directory>
```

2. Create a virtual environment and activate it:
```bash
$ python -m venv venv
$ source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. Install the backend dependencies:
```bash
$ pip install -r requirements.txt
```

4. Install the frontend dependencies:
```bash
$ pip install -r web/requirements_web.txt
```

## Usage

1. Start the FastAPI backend:
```bash
$ uvicorn main:app --reload --port 8080
```

2. Launch the Streamlit interface:
```bash
$ cd web
$ streamlit run frontend.py
```

3. Access the web interface at `http://localhost:8501`

## Key Features

- **Pattern Recognition**: Automatically identifies patterns indicating cancer recurrence
- **Metastasis Detection**: Highlights evidence of metastatic spread
- **Progress Tracking**: Analyzes changes in tumor characteristics over time
- **Treatment Response**: Evaluates responses to various therapeutic interventions
- **Interactive Analysis**: Real-time visualization of findings with detailed annotations

## Analysis Categories

The system focuses on detecting:
1. **Local Recurrence Patterns**
   - Post-surgical site recurrence
   - Regional lymph node involvement
   - Adjacent organ invasion

2. **Distant Metastasis**
   - Liver metastasis
   - Lung metastasis
   - Bone metastasis
   - Other organ involvement

3. **Disease Progression Indicators**
   - Tumor size changes
   - New lesion development
   - Metastatic spread patterns

4. **Treatment Response Markers**
   - Post-treatment changes
   - Therapeutic effectiveness
   - Residual disease assessment

## Technical Details

### API Endpoints

#### POST /search_remote/
Analyzes oncology reports for recurrence patterns using remote LLM service.

##### Request Body:
```json
{
    "report": "Your oncology report text here",
    "api_url": "http://your-llm-service-url",
    "model_name": "llama-3.3-70b-instruct",
    "temperature": 0.85,
    "top_p": 0.3,
    "max_tokens": 2000
}
```

##### Response:
```json
[
    {
        "keyword": "recurrence pattern identified",
        "matches": "matching text from report"
    }
]
```

## Project Structure
```
app/
    models.py      - Data models for cancer analysis
    utils.py       - Core analysis algorithms
    config.py      - Model configuration
    prompts.py     - LLM analysis prompts
web/
    frontend.py    - Interactive web interface
    requirements_web.txt
main.py           - FastAPI application
requirements.txt   - Backend dependencies
```

## Note
This system requires access to a compatible LLM service. While configured for LLaMA models, it can be adapted for other medical-specific language models. Regular updates to the pattern recognition database are recommended to maintain analysis accuracy.
