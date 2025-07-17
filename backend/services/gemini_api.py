import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
API_URL = os.getenv("GEMINI_API_URL")

def analyze_text_with_gemini(extracted_text: str) -> str:
    prompt = f"""
You are a medical AI assistant.

Analyze the following medical report and return a clear, accurate, **structured summary**.

📝 Format the output using clean Markdown:
- Use "## English Summary", "## Kannada Summary", and "## Hindi Summary" as section headers.
- Use proper bullet points (-) for each key point.
- Focus on diagnosis, disease name, key findings, and recommendations only.
- Avoid repeating irrelevant details.

Report:
\"\"\"
{extracted_text}
\"\"\"

Respond with only the markdown-formatted output.
    """

    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    response = requests.post(
        f"{API_URL}?key={API_KEY}",
        json=payload
    )
    response.raise_for_status()
    return response.json()['candidates'][0]['content']['parts'][0]['text']
