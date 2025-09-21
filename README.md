# LLM Knowledge Extractor

A FastAPI-based service that extracts structured data from text using OpenAI's GPT-4o-mini.

## Setup

### Option 1: Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create `.env` file:
```bash
echo "OPENAI_API_KEY=your-api-key-here" > .env
```

3. Run the server:
```bash
uvicorn main:app --reload
```

**Note**: On first run, NLTK will automatically download required data files. This may take a few minutes.

### Option 2: Docker

1. Build the Docker image:
```bash
docker build -t llm-knowledge-extractor .
```

2. Run the container:
```bash
docker run -p 8000:8000 -e OPENAI_API_KEY="your-api-key-here" llm-knowledge-extractor
```

### Option 3: Docker Compose

1. Create `.env` file:
```bash
echo "OPENAI_API_KEY=your-api-key-here" > .env
```

2. Run with Docker Compose:
```bash
docker-compose up --build
```

## Testing the Service

### Web Interface (Recommended)
Once your backend is running on `http://localhost:8000`, you can use the web interface for easy testing:

**[ Open Web Interface](https://llm-summarizer.lovable.app/)**

The web interface automatically connects to your local server on port 8000, providing a user-friendly way to:
- Submit text for analysis
- View extracted summaries, topics, and keywords
- Search through previous analyses
- Test the API without using external tools

### API Documentation
Alternatively, you can use the built-in API documentation:
- Visit `http://localhost:8000/docs` for interactive API testing
- Visit `http://localhost:8000/redoc` for alternative documentation

## API Endpoints

- `POST /analyze` - Analyze text and extract metadata
- `GET /search?topic=xyz` - Search analyses by topic or keyword

## Design Choices

- **FastAPI**: Chosen for its automatic API documentation and type safety
- **SQLite**: Lightweight database perfect for prototyping
- **NLTK**: Reliable NLP library for keyword extraction with graceful fallback
- **Docker**: Containerized for easy deployment and consistency
- **Web Interface**: User-friendly frontend for easy testing and demonstration
- **Modular structure**: Separated concerns into distinct modules for maintainability

## Trade-offs Made

- Used SQLite instead of PostgreSQL for simplicity
- Basic error handling instead of comprehensive logging
- Simple keyword extraction instead of advanced NLP techniques
- Docker for deployment simplicity over Kubernetes
- Graceful fallback for NLTK issues instead of complex setup requirements
- External web interface instead of building a full-stack application

## Troubleshooting

### OpenAI API Errors
- **Quota exceeded**: Check your OpenAI account billing and usage
- **Invalid API key**: Verify your API key in the `.env` file
- **Network issues**: The service will return fallback responses for API failures

### NLTK Issues
- **Data download fails**: The service will automatically fall back to simple keyword extraction
- **Permission errors**: Ensure you have write access to the NLTK data directory

### Web Interface Issues
- **Connection failed**: Ensure your backend is running on `http://localhost:8000`
- **CORS errors**: The backend includes CORS middleware for web interface compatibility

### General Issues
- **Port already in use**: Change the port with `uvicorn main:app --reload --port 8001`
- **Database errors**: Delete `analyses.db` to reset the database
