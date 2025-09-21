from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from keywords import extract_keywords
from llm import call_llm
from db import conn, cursor
import json

app = FastAPI()

class AnalyzeRequest(BaseModel):
    text: str

@app.post("/analyze")
def analyze(req: AnalyzeRequest):
    text = req.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Empty input")

    # Call LLM (with error handling)
    try:
        llm_result = call_llm(text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM processing failed: {str(e)}")

    # Extract keywords
    keywords = extract_keywords(text)

    # Prepare data to store
    summary = llm_result.get("summary", "No summary available")
    title = llm_result.get("title", "No title")
    topics = json.dumps(llm_result.get("topics", []))
    sentiment = llm_result.get("sentiment", "neutral")

    cursor.execute(
        "INSERT INTO analyses (text, summary, title, topics, sentiment, keywords) VALUES (?, ?, ?, ?, ?, ?)",
        (text, summary, title, topics, sentiment, json.dumps(keywords))
    )
    conn.commit()

    return {
        "summary": summary, 
        "title": title, 
        "topics": llm_result.get("topics", []), 
        "sentiment": sentiment, 
        "keywords": keywords
    }

@app.get("/search")
def search(topic: str):
    cursor.execute("SELECT * FROM analyses")
    rows = cursor.fetchall()
    results = []
    for r in rows:
        r_topics = json.loads(r[4])
        r_keywords = json.loads(r[6])
        if topic in r_topics or topic in r_keywords:
            results.append({
                "id": r[0],
                "text": r[1],
                "summary": r[2],
                "title": r[3],
                "topics": r_topics,
                "sentiment": r[5],
                "keywords": r_keywords
            })
    return results
