import streamlit as st
from accessmate.speech import text_to_speech, transcribe_audio
from accessmate.documents import extract_document_text, summarize_or_answer
from accessmate.vision import describe_image
from accessmate.navigation import interpret_command
from accessmate.storage import init_db, save_interaction, get_history, clear_history

st.set_page_config(page_title="AccessMate AI", page_icon="♿", layout="wide")
init_db()

st.markdown("""
<style>
.block-container {padding-top: 1.5rem; max-width: 1150px;}
.stButton button {min-height: 2.7rem;}
</style>
""", unsafe_allow_html=True)

st.title("♿ AccessMate AI")
st.caption("Multimodal Digital Accessibility and Navigation Assistant")
st.info("A student project prototype. AI-generated descriptions and extracted text may contain errors; verify important information.")

with st.sidebar:
    st.header("Navigation")
    page = st.radio("Choose a module", [
        "Home", "1 · Speech Assistant", "2 · Document Reader",
        "3 · Image Understanding", "4 · Voice Navigation", "Interaction History"
    ])
    st.divider()
    st.caption("Gemini features require GEMINI_API_KEY in your environment or Streamlit secrets.")

def record(module, user_input, response):
    save_interaction(module, user_input[:1000], response[:3000])

if page == "Home":
    st.subheader("Your accessibility workspace")
    st.write("Use speech, documents, images, or simple commands to interact with information.")
    cols = st.columns(2)
    cards = [
        ("🔊 Speech Assistant", "Convert written text into spoken audio and transcribe supported audio recordings."),
        ("📄 Document Reader", "Extract text from PDF/DOCX/TXT files, summarize it, and ask questions."),
        ("🖼️ Image Understanding", "Extract visible text and request an AI-generated image description."),
        ("🎙️ Voice Navigation", "Enter or transcribe a spoken command to find the right application module.")
    ]
    for i, (title, desc) in enumerate(cards):
        with cols[i % 2]:
            st.container(border=True).markdown(f"### {title}\n{desc}")
    st.warning("This prototype does not provide emergency guidance, medical diagnosis, or guaranteed navigation for physical spaces.")

elif page == "1 · Speech Assistant":
    st.header("🔊 Speech Assistant")
    st.subheader("Text to speech")
    text = st.text_area("Enter text to read aloud", height=160, placeholder="Type or paste text here...")
    lang = st.selectbox("Speech language", ["en", "hi", "mr", "es", "fr", "de"], format_func=lambda x: {
        "en":"English", "hi":"Hindi", "mr":"Marathi", "es":"Spanish", "fr":"French", "de":"German"
    }[x])
    if st.button("Generate speech", type="primary"):
        if not text.strip():
            st.warning("Enter some text first.")
        else:
            try:
                audio = text_to_speech(text, lang)
                st.audio(audio, format="audio/mp3")
                st.download_button("Download MP3", audio, "accessmate_speech.mp3", "audio/mpeg")
                record("Text to Speech", text, "Audio generated successfully.")
            except Exception as e:
                st.error(f"Could not generate speech: {e}")
    st.divider()
    st.subheader("Audio to text")
    st.write("Upload a WAV, FLAC, or AIFF recording. Speech recognition requires an internet connection.")
    audio_file = st.file_uploader("Choose audio file", type=["wav", "flac", "aiff"])
    if st.button("Transcribe audio"):
        if not audio_file:
            st.warning("Upload an audio file first.")
        else:
            try:
                transcript = transcribe_audio(audio_file)
                st.text_area("Recognized text", transcript, height=150)
                record("Speech to Text", audio_file.name, transcript)
            except Exception as e:
                st.error(f"Transcription failed: {e}")

elif page == "2 · Document Reader":
    st.header("📄 Intelligent Document Reader")
    doc = st.file_uploader("Upload PDF, DOCX, or TXT", type=["pdf", "docx", "txt"])
    if doc:
        try:
            content = extract_document_text(doc)
            st.success(f"Extracted {len(content)} characters.")
            st.text_area("Extracted document text", content, height=250)
            if len(content.strip()) < 30:
                st.warning("Very little text was extracted. If this is a scanned PDF, try uploading page images or use an OCR-enabled PDF.")
            action = st.radio("What would you like to do?", ["Summarize in simple language", "Ask a question"])
            question = ""
            if action == "Ask a question":
                question = st.text_input("Your question about this document")
            if st.button("Process document", type="primary"):
                if action == "Ask a question" and not question.strip():
                    st.warning("Enter a question.")
                elif not content.strip():
                    st.warning("No readable text was found.")
                else:
                    with st.spinner("Processing document..."):
                        answer = summarize_or_answer(content, question if action == "Ask a question" else None)
                    st.markdown("### Result")
                    st.write(answer)
                    record("Document Reader", f"{doc.name}: {action} {question}", answer)
        except Exception as e:
            st.error(f"Could not read this document: {e}")

elif page == "3 · Image Understanding":
    st.header("🖼️ Visual Understanding Agent")
    img = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg", "webp"])
    if img:
        st.image(img, caption="Uploaded image", use_container_width=True)
        task = st.radio("Choose an operation", ["Describe the image", "Extract text from the image"])
        if st.button("Analyze image", type="primary"):
            with st.spinner("Analyzing image..."):
                try:
                    result = describe_image(img.getvalue(), img.type, task)
                    st.markdown("### Result")
                    st.write(result)
                    record("Image Understanding", f"{img.name}: {task}", result)
                except Exception as e:
                    st.error(str(e))

elif page == "4 · Voice Navigation":
    st.header("🎙️ Voice-Based Application Navigation")
    st.write("Type a command, or transcribe an audio recording in the Speech Assistant and paste the recognized words here.")
    command = st.text_input("Enter a command", placeholder="Example: I want to read a PDF")
    if st.button("Understand command", type="primary"):
        if not command.strip():
            st.warning("Enter a command.")
        else:
            result = interpret_command(command)
            st.success(f"Suggested module: {result['module']}")
            st.write(result["guidance"])
            record("Voice Navigation", command, result["guidance"])
    st.caption("This module provides in-app guidance. It does not control your computer or navigate physical streets.")

elif page == "Interaction History":
    st.header("🗂️ Interaction History")
    rows = get_history()
    if rows:
        for module, user_input, response, created in rows:
            with st.expander(f"{created} · {module}"):
                st.markdown("**Input**")
                st.write(user_input)
                st.markdown("**Response**")
                st.write(response)
        if st.button("Clear all history"):
            clear_history()
            st.rerun()
    else:
        st.info("No interactions saved yet.")
