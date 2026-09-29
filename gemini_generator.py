import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai


# Project root folder
BASE_DIR = Path(__file__).resolve().parent.parent

# Load API key from backend/.env
ENV_FILE = BASE_DIR / "backend" / ".env"
load_dotenv(ENV_FILE)

# Read API key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY not found. Please check backend/.env"
    )

# Gemini client
client = genai.Client(api_key=api_key)


def generate_legal_document(
    document_type,
    parties,
    terms,
    dates
):
    prompt = f"""
You are a professional legal document drafting assistant.

Create a professional legal document based on the information below.

Document Type:
{document_type}

Parties:
{parties}

Important Terms:
{terms}

Dates:
{dates}

Requirements:
- Use a clear professional legal format.
- Add suitable headings.
- Add appropriate clauses.
- Include the important terms provided by the user.
- Include a signature section.
- Do not invent important personal information.
- Make the document easy to read and edit.
"""

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt
    )

    return response.text