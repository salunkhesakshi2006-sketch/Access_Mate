
import os
import streamlit as st
from google import genai
from google.genai import types


def get_client():
    """Create and return the Gemini API client."""

    api_key = os.getenv("GEMINI_API_KEY", "").strip()

    if not api_key:
        try:
            api_key = st.secrets.get("GEMINI_API_KEY", "").strip()
        except Exception:
            api_key = ""

    if not api_key:
        raise ValueError(
            "Gemini API key is missing. "
            "Add GEMINI_API_KEY to Streamlit secrets."
        )

    return genai.Client(api_key=api_key)


def get_model():
    """Get the Gemini model name."""

    model = os.getenv("GEMINI_MODEL", "").strip()

    if not model:
        try:
            model = st.secrets.get(
                "GEMINI_MODEL",
                "gemini-3.8-flash"
            ).strip()
        except Exception:
            model = "gemini-3.8-flash"

    return model


def ask_gemini(prompt, image_bytes=None, mime_type="image/jpeg"):
    """Send text or image input to Gemini and return its response."""

    try:
        client = get_client()

        contents = [prompt]

        if image_bytes:
            image_part = types.Part.from_bytes(
                data=image_bytes,
                mime_type=mime_type
            )
            contents.append(image_part)

        response = client.models.generate_content(
            model=get_model(),
            contents=contents
        )

        return response.text or "No response generated."

    except Exception as error:
        error_text = str(error)

        if (
            "429" in error_text
            or "RESOURCE_EXHAUSTED" in error_text
            or "quota" in error_text.lower()
        ):
            raise RuntimeError(
                "Daily Gemini API quota exceeded. "
                "Please try again after the quota resets."
            ) from error

        if "503" in error_text or "UNAVAILABLE" in error_text:
            raise RuntimeError(
                "Gemini service is temporarily unavailable. "
                "Please try again later."
            ) from error

        raise RuntimeError(
            f"Gemini request failed: {error_text}"
        ) from error
