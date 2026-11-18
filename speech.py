from io import BytesIO

def text_to_speech(text, language="en"):
    from gtts import gTTS
    buffer = BytesIO()
    gTTS(text=text, lang=language, slow=False).write_to_fp(buffer)
    return buffer.getvalue()

def transcribe_audio(uploaded_file):
    import speech_recognition as sr
    recognizer = sr.Recognizer()
    audio_data = uploaded_file.getvalue()
    import tempfile, os
    suffix = "." + uploaded_file.name.rsplit(".", 1)[-1].lower()
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp:
        temp.write(audio_data)
        path = temp.name
    try:
        with sr.AudioFile(path) as source:
            audio = recognizer.record(source)
        return recognizer.recognize_google(audio)
    finally:
        os.unlink(path)
