
from accessmate.ai import ask_gemini


def describe_image(
    image_bytes,
    mime_type="image/jpeg",
    operation="Describe the image"
):
    """Describe an image or extract its visible text."""

    if not image_bytes:
        return "Please upload an image first."

    try:
        if operation == "Describe the image":
            prompt = """
            Describe this image in simple, clear language.

            Include:
            1. Main objects and people.
            2. Colors and surroundings.
            3. Important visible details.
            4. Details useful for accessibility.

            Do not guess unclear information.
            """

        elif operation == "Extract text from the image":
            prompt = """
            Extract all visible text from this image.

            Instructions:
            1. Preserve original wording.
            2. Maintain reading order.
            3. Preserve headings and numbers.
            4. Mark unclear text as [Unclear text].
            5. Do not invent missing words.
            """

        else:
            return "Invalid image operation selected."

        result = ask_gemini(
            prompt,
            image_bytes=image_bytes,
            mime_type=mime_type
        )

        return result or "No result generated."

    except Exception as error:
        error_message = str(error)

        if (
            "429" in error_message
            or "RESOURCE_EXHAUSTED" in error_message
            or "quota" in error_message.lower()
        ):
            return (
                "Daily Gemini quota exceeded. "
                "Please try again after the quota resets."
            )

        if "503" in error_message or "UNAVAILABLE" in error_message:
            return "Gemini service is temporarily unavailable. Please try again later."

        return f"Image processing failed: {error_message}"


def extract_image_text(image_bytes, mime_type="image/jpeg"):
    return describe_image(
        image_bytes,
        mime_type,
        "Extract text from the image"
    )
