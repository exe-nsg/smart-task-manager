import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def analyze_task(title: str, description: str = "") -> dict:

    prompt = f"""
    You are an expert productivity coach with 10 years experience.

    Analyze this task and provide detailed smart insights:

    TASK TITLE: {title}
    TASK DESCRIPTION: {description}

    Return ONLY this exact JSON:
    {{
        "priority_score": <number 1-100>,
        "estimated_time": "<e.g. 30 minutes or 2 hours>",
        "category": "<Academic, Work, Personal, Health, Finance, Creative, or Other>",
        "difficulty_level": "<Easy, Medium, or Hard>",
        "energy_required": "<Low, Medium, or High>",
        "deadline_sensitivity": "<Urgent, Normal, or Flexible>",
        "best_time": "<Early Morning, Morning, Afternoon, Evening, or Anytime>",
        "suggestion": "<one specific actionable tip for this task>",
        "motivation": "<one powerful motivational sentence specific to this task>",
        "steps": [
            "<step 1>",
            "<step 2>",
            "<step 3>"
        ]
    }}

    Return ONLY the JSON. No extra text.
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

    return json.loads(response_text)


def get_fallback_analysis(title: str) -> dict:
    return {
        "priority_score": 50,
        "estimated_time": "1 hour",
        "category": "General",
        "difficulty_level": "Medium",
        "energy_required": "Medium",
        "deadline_sensitivity": "Normal",
        "best_time": "Morning",
        "suggestion": f"Break '{title}' into smaller steps and tackle one at a time",
        "motivation": f"Every big achievement starts with the decision to try. You've got this!",
        "steps": [
            "Plan your approach before starting",
            "Focus on one section at a time",
            "Review your work when finished"
        ]
    }
