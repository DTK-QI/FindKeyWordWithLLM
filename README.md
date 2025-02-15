# Cancer Report Analysis

This project provides a comprehensive solution for analyzing medical reports using advanced language models and a user-friendly web interface.

## Components

### 1. FastAPI Backend
- Provides API endpoints for medical report analysis
- Uses LLaMA model for text processing
- Handles both local and remote LLM processing

### 2. Streamlit Web Interface
- User-friendly interface for report analysis
- Real-time text highlighting
- Configurable model parameters
- Visual result presentation

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

## API Endpoints

### POST /search_remote/
Analyzes medical reports using a remote LLM service.

#### Request Body:
```json
{
    "report": "Your medical report text here",
    "api_url": "http://your-llm-service-url",
    "model_name": "llama-3.3-70b-instruct",
    "temperature": 0.85,
    "top_p": 0.3,
    "max_tokens": 2000
}
```

#### Response:
```json
[
    {
        "keyword": "keyword found",
        "matches": "matching sentence from report"
    }
]
```

## Project Structure
```
app/
    models.py      - Data models and request schemas
    utils.py       - Core analysis functionality
    config.py      - Model configuration
    prompts.py     - LLM prompts
web/
    frontend.py    - Streamlit web interface
    requirements_web.txt
main.py           - FastAPI application
requirements.txt   - Backend dependencies
```

## Features
- Automatic keyword detection in medical reports
- Support for both local and remote LLM processing
- Interactive text highlighting
- Configurable model parameters
- Real-time analysis results
- User-friendly web interface

## Predefined Keywords
The system automatically searches for patterns related to:
- Cancer metastasis (liver, lung, bone)
- Recurrent tumors
- Cancer progression
- Treatment responses
- Medical terminology specific to cancer diagnosis

## Note
Make sure you have access to the LLM service (local or remote) before running the application. The system is configured to work with LLaMA models but can be adapted for other LLMs.
