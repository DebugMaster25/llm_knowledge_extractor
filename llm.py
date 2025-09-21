import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def call_llm(text: str):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{
                "role": "user", 
                "content": f"""Analyze this text and return a JSON response with exactly this format:
                {{
                    "summary": "1-2 sentence summary here",
                    "title": "extracted or generated title here",
                    "topics": ["topic1", "topic2", "topic3"],
                    "sentiment": "positive"
                }}
                
                Text to analyze: {text}"""
            }]
        )
        
        # Parse JSON response
        content = response.choices[0].message.content
        return json.loads(content)
        
    except Exception as e:
        # Handle LLM API failure as required by assignment
        print(f"LLM API error: {e}")
        return {
            "summary": "Analysis failed due to API error",
            "title": "Error",
            "topics": ["error"],
            "sentiment": "neutral"
        }


# def call_llm(text: str):
#     return {
#         "summary": "Mock summary.",
#         "title": "Mock Title",
#         "topics": ["topic1", "topic2", "topic3"],
#         "sentiment": "neutral"
#     }
