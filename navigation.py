def interpret_command(command):
    text = command.lower()
    rules = [
        (["speech", "speak", "read aloud", "audio", "voice to text", "transcribe"], "Speech Assistant",
         "Open Speech Assistant. Use Text to Speech to hear typed text, or upload a WAV/FLAC/AIFF recording for transcription."),
        (["pdf", "document", "docx", "summarize", "file", "question about"], "Document Reader",
         "Open Document Reader, upload a PDF, DOCX, or TXT file, then choose summary or question-answering."),
        (["image", "photo", "picture", "visual", "ocr"], "Image Understanding",
         "Open Image Understanding, upload a supported image, and choose image description or text extraction."),
        (["history", "previous", "past"], "Interaction History",
         "Open Interaction History to review saved module interactions or clear the history."),
    ]
    for keywords, module, guidance in rules:
        if any(word in text for word in keywords):
            return {"module": module, "guidance": guidance}
    return {
        "module": "Home Dashboard",
        "guidance": "I could not match that command. Try: 'read a PDF', 'describe an image', 'speak this text', or 'show history'."
    }
