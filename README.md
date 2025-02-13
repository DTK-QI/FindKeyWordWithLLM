# Medical Report Keyword Search API

## API Endpoints

### 1. Get Keywords
```
GET http://localhost:8000/keywords/
```

### 2. Search Reports
```
POST http://localhost:8000/search/
Content-Type: application/json
```

Parameters:
- similarity_threshold: Similarity threshold (optional, default 0.7)
- max_results: Maximum number of results (optional, default 10)

### Request Format

Basic Format:
```json
{
  "reports": [
    { "content": "Report content 1" },
    { "content": "Report content 2" }
  ]
}
```

Example:
```json
{
  "reports": [
    { 
      "content": "Imaging Report: Chest CT. Findings: 2.5cm nodule in right upper lobe, mediastinal lymphadenopathy. Conclusion: Suspected recurrence"
    },
    {
      "content": "Pathology Report: Lung adenocarcinoma, moderately differentiated, tumor cell invasion observed"
    }
  ]
}
```

### Response Format

Successful Response (200 OK):
```json
{
  "results": [
    {
      "keyword": "lung adenocarcinoma",
      "matches": [
        {
          "text": "Pathology Report: Lung adenocarcinoma, moderately differentiated",
          "similarity_score": 0.92
        }
      ]
    },
    {
      "keyword": "lymphadenopathy",
      "matches": [
        {
          "text": "2.5cm nodule in right upper lobe, mediastinal lymphadenopathy",
          "similarity_score": 0.88
        }
      ]
    }
  ]
}
```

Error Response (400 Bad Request):
```json
{
  "detail": "No matching results found"
}
```

## Service Setup
```bash
uvicorn main:app --reload
```

API Documentation: http://localhost:8000/docs