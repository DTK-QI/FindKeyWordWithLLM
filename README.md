# Cancer Report Analysis API

This FastAPI application provides an API for analyzing cancer reports using the Llama 3.2 3B model and LlamaIndex. The system automatically searches for predefined cancer-related keywords and patterns in the provided medical reports.

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

3. Install the required dependencies:
```bash
$ pip install -r requirements.txt
```

## Usage

1. Run the FastAPI application:
```bash
$ uvicorn main:app --reload
```

2. The API will be available at `http://localhost:8080`.

## API Endpoints

### POST /search/

Analyzes a medical report for predefined cancer-related patterns and keywords.

#### Request Body

```json
{
    "report": "Your medical report text here"
}
```

#### Response

Returns a list of matches for each predefined keyword found in the report:

```json
[
    {
        "keyword": "liver metastasis",
        "matches": [
            "Patient shows signs of liver metastasis",
            "Similar patterns suggesting liver involvement"
        ],
        "extracted_info": []
    },
    {
        "keyword": "recurrent rectal cancer",
        "matches": [
            "Symptoms indicate recurrent rectal cancer"
        ],
        "extracted_info": []
    }
]
```

## Project Structure

```
app/
    __pycache__/
    models.py     - Data models and request/response schemas
    utils.py      - Core functionality and predefined keywords
main.py          - FastAPI application and routes
requirements.txt - Project dependencies
```

## Predefined Keywords

The system automatically searches for patterns related to:
- Metastasis (liver, lung, bone)
- Recurrent tumors
- Cancer progression
- Treatment responses
- And more specific medical terminology

No need to specify keywords in the request - the system uses a comprehensive set of predefined medical terms and patterns.
