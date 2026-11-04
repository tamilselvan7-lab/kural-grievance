
import os
import json
import time
import logging
from functools import lru_cache

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

# Faster model for translation and classification
MODEL_NAME = "gemini-3.5-flash-lite"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DEPARTMENTS = [
    "Water",
    "Roads",
    "Electricity",
    "Sanitation",
    "Healthcare",
    "Public Safety",
    "Education",
    "Other",
]

RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "detected_language": {
            "type": "string",
        },
        "translated_complaint": {
            "type": "string",
        },
        "department": {
            "type": "string",
            "enum": DEPARTMENTS,
        },
        "priority_score": {
            "type": "integer",
            "minimum": 0,
            "maximum": 100,
        },
        "priority_reason": {
            "type": "string",
        },
    },
    "required": [
        "detected_language",
        "translated_complaint",
        "department",
        "priority_score",
        "priority_reason",
    ],
}


@lru_cache(maxsize=1)
def get_gemini_client():
    """Create and reuse one Gemini client."""

    if not API_KEY:
        raise ValueError(
            "Gemini API key not found. Set GEMINI_API_KEY."
        )

    return genai.Client(
        api_key=API_KEY,
        http_options=types.HttpOptions(
            timeout=20000,
            retry_options=types.HttpRetryOptions(
                attempts=1
            ),
        ),
    )


def analyze_complaint(complaint_text):
    """
    Detect language, translate, classify and prioritize
    a citizen grievance using Gemini Flash-Lite.

    Keeps the same return structure expected by app.py.
    """

    if not complaint_text or not complaint_text.strip():
        raise ValueError("Complaint cannot be empty.")

    client = get_gemini_client()
    complaint_text = complaint_text.strip()

    prompt = f"""
Analyze this Indian citizen grievance.

Return:
1. Original language name in English.
2. Complete and accurate English translation.
3. Exactly one department from: {", ".join(DEPARTMENTS)}.
4. Priority score from 0 to 100.
5. One short reason for the score.

Priority guidance:
0-20: Low
21-40: Normal
41-60: Moderate
61-80: High
81-100: Critical

Consider severity, public health, safety, affected people
and duration. Do not invent facts or assume emergencies.
A brief complaint must still be classified.

Complaint:
{complaint_text}
"""

    start_time = time.perf_counter()

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_json_schema=RESPONSE_SCHEMA,
                thinking_config=types.ThinkingConfig(
                    thinking_level="minimal"
                ),
                max_output_tokens=256,
            ),
        )

        if not response.text:
            raise ValueError("Gemini returned an empty response.")

        result = json.loads(response.text)

        # Validate required fields
        required_fields = [
            "detected_language",
            "translated_complaint",
            "department",
            "priority_score",
            "priority_reason",
        ]

        for field in required_fields:
            if field not in result:
                raise ValueError(f"Missing AI field: {field}")

        result["detected_language"] = str(
            result["detected_language"]
        )
        result["translated_complaint"] = str(
            result["translated_complaint"]
        )
        result["priority_reason"] = str(
            result["priority_reason"]
        )

        result["priority_score"] = int(
            result["priority_score"]
        )

        if not 0 <= result["priority_score"] <= 100:
            raise ValueError("Invalid priority score.")

        if result["department"] not in DEPARTMENTS:
            raise ValueError("Invalid department returned.")

        elapsed = time.perf_counter() - start_time

        logger.info(
            "Complaint analyzed | Model: %s | Time: %.2f seconds",
            MODEL_NAME,
            elapsed,
        )

        return result

    except Exception as error:
        elapsed = time.perf_counter() - start_time

        logger.exception(
            "Complaint analysis failed after %.2f seconds",
            elapsed,
        )

        raise RuntimeError(
            f"Complaint analysis failed: {error}"
        ) from error   