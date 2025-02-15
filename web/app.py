from flask import Flask, request, jsonify
from sys import path
from pathlib import Path
import asyncio
path.append(str(Path(__file__).parent.parent))

from app.utils import search_report
from app.models import SearchRequest

app = Flask(__name__)

@app.route('/extract_keywords', methods=['POST'])
async def extract_keywords():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400
    
    data = request.get_json()
    text = data.get('text', '')
    
    if not text:
        return jsonify({"error": "Text is required"}), 400
    
    # Create a SearchRequest object to reuse existing functionality
    search_request = SearchRequest(report=text)
    results = await search_report(search_request)
    
    # Convert results to the required format
    formatted_results = [
        {
            "keyword": result.keyword,
            "matches": result.matches[0] if result.matches else ""
        }
        for result in results
    ]
    
    return jsonify(formatted_results)

def run_flask():
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    run_flask()