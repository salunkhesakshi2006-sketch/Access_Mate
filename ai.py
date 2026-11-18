import os
import time
import streamlit as st
from pathlib import Path
from google import genai
from google.genai import types
from gtts import gTTS

import os
import streamlit as st
from google import genai


def get_client():
    api_key = os.getenv("GEMINI_API_KEY", "")

    if not api_key:
        try:
            api_key = st.secrets.get("GEMINI_API_KEY", "")
        except Exception:
            api_key = ""

    if not api_key:
        raise ValueError("Gemini API key is missing.")

    return genai.Client(api_key=api_key)




def ask_gemini(prompt, image_bytes=None, mime_type="image/jpeg"):
    client = get_client()

    contents = [prompt]

    if image_bytes:
        contents.append(
            types.Part.from_bytes(
                data=image_bytes,
                mime_type=mime_type
            )
        )

    for attempt in range(5):
        try:
            response = client.models.generate_content(
                model=get_model(),
                contents=contents
            )

            return response.text or "No response generated."

        except Exception as e:
                error_text = str(e)

                if "429" in error_text or "RESOURCE_EXHAUSTED" in error_text:
                    raise RuntimeError(
                        "Daily Gemini quota exceeded. "
                        "Please try again after the quota resets."
        )

        raise RuntimeError(f"Gemini request failed: {e}")

def get_model():
    model = os.getenv("GEMINI_MODEL", "").strip()

    if not model:
        try:
            model = st.secrets.get(
                "GEMINI_MODEL",
                "gemini-3.8-flash"
            )
        except Exception:
            model = "gemini-3.8-flash"

    return model
