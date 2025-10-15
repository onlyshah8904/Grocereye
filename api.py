# api.py
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import uvicorn
from scraper import scraper
from blinkit import get_session as blinkit_session
from bigbasket import get_session as bb_session
from configs import API_KEY
import requests as http_requests
import json

app = FastAPI()

@app.get("/keywords")
async def get_keywords(query: str = Query(...)):
    if not query.strip():
        return {"keywords": []}

    instruction = f"""
You are a shopping intent analyzer. Extract only grocery product keywords.
Rules:
- Return ONLY a JSON array of lowercase strings.
- Use synonyms: "chocolates" → "chocolate", "hungry" → "snacks"
- Avoid verbs, adjectives.

Input: {query.strip()}
Output (JSON only):
"""

    headers = {
        'Content-Type': 'application/json',
        'X-goog-api-key': API_KEY,
    }

    json_data = {
        "contents": [{"parts": [{"text": instruction}]}],
        "generationConfig": {
            "temperature": 0.2,
            "topP": 0.9,
            "maxOutputTokens": 100,
            "responseMimeType": "application/json"
        }
    }

    url = "https://generativelanguage.googleapis.com/v1/models/gemini-2.0-flash:generateContent"

    try:
        response = http_requests.post(url, headers=headers, json=json_data)
        if response.status_code != 200:
            return {"keywords": []}

        data = response.json()
        raw_text = data['candidates'][0]['content']['parts'][0]['text'].strip()
        keywords = json.loads(raw_text)
        return {"keywords": [kw.strip().lower() for kw in keywords if kw.strip()]}
    except Exception as e:
        print("Gemini error:", e)
        return {"keywords": []}

@app.post("/init-location")
async def init_location(pincode: str = Query(...)):
    bb = bb_session(pincode)
    bl = blinkit_session(pincode)
    if bb or bl:
        return {"message": "Location set", "pincode": pincode}
    return JSONResponse(status_code=400, content={"error": "Failed to set location"})

@app.get("/search")
async def search(keyword: str = Query(...), pincode: str = Query(...)):
    results = scraper(keyword, pincode)
    return {"keyword": keyword, "pincode": pincode, "results": results}

if __name__ == "__main__":
    uvicorn.run("api:app", host="127.0.0.1", port=8900, workers=1)