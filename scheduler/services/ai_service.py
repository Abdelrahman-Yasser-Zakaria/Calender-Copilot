import os
import json
import google.generativeai as genai
from django.conf import settings

def parse_availability_with_gemini(text):
    """
    Parses natural language availability into a structured JSON using Gemini.
    """
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        return {"error": "GOOGLE_API_KEY not configured"}

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash') # Using 1.5 Flash as 3 Flash might not be available in SDK yet, or sticking to standard stable models

    system_instruction = """
    Role: You are a calendar scheduling assistant.
    Task: Convert the user's natural language availability description into a structured JSON array.
    Format:
    [
      {"day": "Monday", "start_time": "HH:MM AM/PM", "end_time": "HH:MM AM/PM"},
      ...
    ]
    Rules:
    - Use 12-hour format (e.g., 07:00 PM, 12:00 AM).
    - Identify specific days. "Weekends" = Friday, Saturday.
    - "Noon" = 12:00 PM, "Midnight" = 12:00 AM.
    - Return ONLY valid JSON. No markdown formatting.
    """

    prompt = f"{system_instruction}\n\nUser Input: {text}"

    try:
        response = model.generate_content(prompt)
        # Clean up response text to ensure it's just JSON
        content = response.text.strip()
        if content.startswith('```json'):
            content = content[7:]
        if content.endswith('```'):
            content = content[:-3]
        content = content.strip()
        
        parsed_data = json.loads(content)
        return parsed_data
    except Exception as e:
        return {"error": str(e)}

