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
        
        # Get the content and debug
        content = response.choices[0].message.content
        print(f"LLM Response: {repr(content)}")  # Debug line

        # Clean up the response (remove markdown code blocks if present)
        if content.startswith("```json"):
            content = content[7:]
        elif content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]

        content = content.strip()

        # Check if content is empty
        if not content or not content.strip():
            print("Empty response from LLM")
            return {
                "summary": "Empty response from LLM",
                "title": "Error",
                "topics": ["error"],
                "sentiment": "neutral"
            }
        
        # Try to parse JSON
        try:
            return json.loads(content)
        except json.JSONDecodeError as json_err:
            print(f"JSON parsing error: {json_err}")
            print(f"Raw content: {content}")
            return {
                "summary": "Invalid JSON response from LLM",
                "title": "Error",
                "topics": ["error"],
                "sentiment": "neutral"
            }
        
    except Exception as e:
        # Handle LLM API failure as required by assignment
        print(f"LLM API error: {e}")
        return {
            "summary": "Analysis failed due to API error",
            "title": "Error",
            "topics": ["error"],
            "sentiment": "neutral"
        }

# Mock version (commented out)
# def call_llm(text: str):
#     return {
#         "summary": f"This is a mock summary for: {text[:50]}...",
#         "title": "Mock Title",
#         "topics": ["technology", "artificial intelligence", "machine learning"],
#         "sentiment": "positive"
#     }
