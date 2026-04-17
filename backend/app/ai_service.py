import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def analyze_task(title: str, description: str = "") -> dict:

    prompt = f"""
    You are an expert productivity coach with 10 years experience.

    Analyze this task and provide smart insights:

    TASK TITLE: {title}
    TASK DESCRIPTION: {description}

    Return your analysis in this EXACT JSON format:
    {{
        "priority_score": <number between 1 and 100>,
        "estimated_time": "<realistic time estimate like 30 minutes or 2 hours>",
        "category": "<one of: Academic, Work, Personal, Health, Finance, Other>",
        "suggestion": "<one specific actionable advice for this task>",
        "best_time": "<one of: Morning, Afternoon, Evening, Anytime>"
    }}

    Return ONLY the JSON. No extra text before or after.
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a productivity expert. Always respond with valid JSON only."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    response_text = response.choices[0].message.content.strip()

    if response_text.startswith("```"):
        response_text = response_text.split("```")[1]
        if response_text.startswith("json"):
            response_text = response_text[4:]

    analysis = json.loads(response_text)
    return analysis


def get_fallback_analysis(title: str) -> dict:
    return {
        "priority_score": 50,
        "estimated_time": "1 hour",
        "category": "General",
        "suggestion": f"Break '{title}' into smaller steps and tackle one at a time",
        "best_time": "Morning"
    }
