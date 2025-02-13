import pytest
from fastapi.testclient import TestClient
from app.main import app
import io

client = TestClient(app)

def create_test_file(content: str):
    return io.BytesIO(content.encode())

def test_upload_keywords():
    test_content = "keyword1\nkeyword2\nkeyword3"
    file = create_test_file(test_content)
    response = client.post(
        "/upload_keywords/",
        files={"file": ("test.txt", file, "text/plain")}
    )
    assert response.status_code == 200
    assert "Successfully uploaded" in response.json()["message"]

def test_upload_corpus():
    test_content = "This is a test corpus. It contains some text for testing."
    file = create_test_file(test_content)
    response = client.post(
        "/upload_corpus/",
        files={"file": ("test.txt", file, "text/plain")}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Successfully uploaded and indexed corpus"

def test_search_without_uploads():
    response = client.post("/search/")
    assert response.status_code == 400

def test_invalid_file_type():
    file = create_test_file("test content")
    response = client.post(
        "/upload_keywords/",
        files={"file": ("test.pdf", file, "application/pdf")}
    )
    assert response.status_code == 400

def test_search_with_uploads():
    # Upload keywords first
    keywords = "test\nexample\nsample"
    keyword_file = create_test_file(keywords)
    response = client.post(
        "/upload_keywords/",
        files={"file": ("keywords.txt", keyword_file, "text/plain")}
    )
    assert response.status_code == 200

    # Upload corpus
    corpus = "This is a test document. It contains example text and sample content."
    corpus_file = create_test_file(corpus)
    response = client.post(
        "/upload_corpus/",
        files={"file": ("corpus.txt", corpus_file, "text/plain")}
    )
    assert response.status_code == 200

    # Perform search
    response = client.post("/search/", params={"similarity_threshold": 0.5, "max_results": 5})
    assert response.status_code == 200
    results = response.json()["results"]
    assert isinstance(results, list)
    for result in results:
        assert "keyword" in result
        assert "matches" in result