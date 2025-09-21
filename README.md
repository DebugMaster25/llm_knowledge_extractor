# LLM Knowledge Extractor

A FastAPI-based service that extracts structured data from text using OpenAI's GPT-4o-mini.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set OpenAI API key:
```bash
export OPENAI_API_KEY="your-api-key-here"
```

3. Run the server:
```bash
uvicorn main:app --reload
```

## API Endpoints

- `POST /analyze` - Analyze text and extract metadata
  - Request body: `{"text": "Your text here"}`
  - Returns: summary, title, topics, sentiment, keywords

- `GET /search?topic=xyz` - Search analyses by topic or keyword
  - Returns: All analyses matching the topic/keyword

## Design Choices

- **FastAPI**: Chosen for its automatic API documentation and type safety with Pydantic models
- **SQLite**: Lightweight database perfect for prototyping, no external dependencies
- **NLTK**: Reliable NLP library for keyword extraction using POS tagging
- **Modular structure**: Separated concerns into distinct modules (llm.py, keywords.py, db.py) for maintainability
- **Error handling**: Graceful degradation when LLM API fails, returns error message instead of crashing

## Trade-offs Made

- Used SQLite instead of PostgreSQL for simplicity and zero setup
- Basic error handling instead of comprehensive logging system
- Simple keyword extraction using noun frequency instead of advanced NLP techniques
- No authentication/rate limiting for prototype simplicity
- No caching layer to keep it lightweight

## Core Requirements Met

✅ Text input processing  
✅ LLM integration with structured JSON output  
✅ Keyword extraction (3 most frequent nouns)  
✅ SQLite persistence  
✅ REST API with analyze and search endpoints  
✅ Error handling for empty input and LLM failures  
✅ 1-2 sentence summaries  
✅ Structured metadata extraction
