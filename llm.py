import os
from pathlib import Path
from groq import Groq
from dotenv import load_dotenv

env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

# Get key
api_key = os.getenv("GROQ_API_KEY")

# Debug (temporary)
print("API KEY:", api_key)

if not api_key:
    raise ValueError("❌ GROQ_API_KEY not found. .env not loading.")

# Initialize client
client = Groq(api_key=api_key)

def analyze_resume(resume_text, job_role, past_memory=""):
    prompt = f"""
You are an AI career mentor.
Past attempts:
{past_memory}
Analyze this resume for the role: {job_role}

Resume:
{resume_text}

Give output in this EXACT format:

Skill Gaps:
- ...

Suggestions:
- ...

Improvements:
- Formatting: ...
- Objective: ...
- Projects: ...
- Skills: ...

IMPORTANT:
- Only plain text
- No HTML
- No <div>, <span>
- No markdown like ** or ##

Also give a confidence score from 0 to 100 based on how well the resume matches the job role.

Format:
Score: <number>

- Compare with past attempts
- Highlight improvement or decline
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


def split_sections(text):
    sections = {
        "Skill Gaps": "",
        "Suggestions": "",
        "Improvements": ""
    }

    current = None

    for line in text.split("\n"):
        line = line.strip()

        if "Skill Gaps" in line:
            current = "Skill Gaps"
            continue
        elif "Suggestions" in line:
            current = "Suggestions"
            continue
        elif "Improvements" in line:
            current = "Improvements"
            continue

        if current:
            sections[current] += line + "<br>"

    return sections