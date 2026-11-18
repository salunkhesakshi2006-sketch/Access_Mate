# AccessMate AI
Multimodal Digital Accessibility and Navigation Agent — Python + Streamlit + Gemini.

## Included working phases

1. **Speech Assistant:** Text-to-speech using gTTS; audio-to-text for WAV/FLAC/AIFF using SpeechRecognition.
2. **Document Reader:** Extracts text from PDF, DOCX and TXT; Gemini-powered summary and document Q&A.
3. **Image Understanding:** Gemini image descriptions and image text extraction.
4. **Voice Navigation:** Understands common typed commands and directs the user to the correct in-app module. For spoken commands, transcribe audio in Module 1 and paste the result here.
5. **History:** Stores recent interactions locally in SQLite and allows clearing history.

> This is a working student prototype, not a certified assistive technology product. It does not control a computer or provide physical-world navigation. AI results and OCR/transcription can be incorrect; review important information.

## 1. Requirements

- Python 3.10 or newer (Python 3.12 is suitable)
- Internet connection for package installation, Gemini, gTTS and online speech recognition
- A Gemini API key for document summaries/Q&A and image understanding

## 2. Install on Windows

Extract the ZIP, open Command Prompt in the `AccessMate_AI` folder, then run:

```bash
py -3.12 -m venv .venv
.venv\\Scripts\\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If Python 3.12 is not installed, use `python -m venv .venv` instead.

## 3. Configure Gemini

Set your API key in the same Command Prompt session:

```bat
set GEMINI_API_KEY=YOUR_ACTUAL_API_KEY
```

Optional model override:

```bat
set GEMINI_MODEL=gemini-2.5-flash
```

Get your own key from Google AI Studio. Never share it or upload it to a public GitHub repository.

Alternatively, copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml` and replace the placeholder with your key. Do not publish that file.

## 4. Run

```bash
streamlit run app.py
```

Streamlit will print a local URL, usually `http://localhost:8501`.

## 5. Test each module

- Speech: type a short sentence and generate MP3; upload a supported audio recording to transcribe.
- Document: upload a text-based PDF, DOCX or TXT; test summary and question-answering.
- Image: upload a JPG or PNG and request description or text extraction.
- Navigation: try `I want to read a PDF`, `describe this image`, `speak this text`, and `show history`.
- History: verify entries appear and test Clear all history.

## 6. Common errors

**Gemini API key missing:** Set `GEMINI_API_KEY` and restart the Streamlit process.

**Model not found / unavailable:** Set `GEMINI_MODEL` to a model currently enabled for your Google AI Studio key. Model availability can change by account and region.

**Speech recognition error:** Use a clear WAV/FLAC/AIFF recording and ensure internet access. The Google recognition endpoint used by SpeechRecognition is an online service and may have usage limits.

**PDF has no extracted text:** It may be a scanned document. This starter version extracts embedded PDF text; it does not include OCR for scanned PDF pages. Save the page as an image and use the Image Understanding module.

**gTTS error:** Check internet connectivity; gTTS uses an online service.

## 7. Project structure

```text
AccessMate_AI/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── .streamlit/
│   └── secrets.toml.example
└── accessmate/
    ├── __init__.py
    ├── ai.py
    ├── speech.py
    ├── documents.py
    ├── vision.py
    ├── navigation.py
    └── storage.py
```

## 8. Suggested future enhancements

- Add OCR for scanned multi-page PDFs using Tesseract.
- Add true microphone-based continuous voice navigation.
- Add keyboard shortcuts, screen-reader testing and WCAG-informed UI checks.
- Add user accounts and encrypted storage only if genuinely required.
- Evaluate transcription accuracy, extraction quality, task completion rate and response time with consented test users.

## Privacy

The prototype saves interaction text in a local SQLite database. Do not upload confidential, medical, identity, financial or otherwise sensitive documents. Gemini requests send the relevant prompt/document excerpt or image to Google's API. Review the provider's current privacy and data-use terms before using real user data.
