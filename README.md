# Pattern Analysis System

This system provides a comprehensive solution for analyzing text patterns and extracting relevant information using advanced language models.

## Overview

This tool is designed to assist in:
- Detecting important patterns
- Identifying key information
- Analyzing textual content
- Evaluating content relationships
- Monitoring changes and trends

## Components

### 1. FastAPI Backend
- Specialized API endpoints for text analysis
- Advanced pattern recognition using LLaMA model
- Supports both local and remote processing

### 2. Streamlit Web Interface
- Intuitive interface for text analysis
- Real-time highlighting of findings
- Interactive visualization
- Configurable parameters

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

- **Pattern Recognition**: Automatically identifies important patterns
- **Content Analysis**: Highlights relevant information
- **Progress Tracking**: Analyzes changes over time
- **Response Analysis**: Evaluates content relationships
- **Interactive Analysis**: Real-time visualization with detailed annotations

## Analysis Categories

The system focuses on detecting:
1. **Key Patterns**
   - Primary indicators
   - Related elements
   - Connected components

2. **Information Relationships**
   - Direct connections
   - Indirect relationships
   - Pattern associations

3. **Progress Indicators**
   - Change patterns
   - Development indicators
   - Trend analysis

4. **Response Markers**
   - Pattern changes
   - Effect indicators
   - Progress assessment

## Technical Details

### API Endpoints

#### POST /search_remote/
Analyzes text for patterns using remote LLM service.

##### Request Body:
```json
{
    "report": "Your text content here",
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
        "keyword": "pattern identified",
        "matches": "matching text from content"
    }
]
```

## Project Structure
```
app/
    models.py      - Data models
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
This system requires access to a compatible LLM service. While configured for LLaMA models, it can be adapted for other language models. Regular updates to the pattern recognition database are recommended to maintain analysis accuracy.
