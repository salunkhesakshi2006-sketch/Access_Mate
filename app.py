
import streamlit as st

st.set_page_config(
    page_title="AccessMate AI",
    page_icon="♿",
    layout="wide"
)

st.title("♿ AccessMate AI Agent")

st.subheader("Your Multimodal Digital Accessibility Assistant")

st.write(
    "Welcome! AccessMate AI helps users access "
    "digital information using Artificial Intelligence."
)

st.success("AccessMate AI application is running!")

st.markdown("---")

st.subheader("Choose an AI Assistant")

col1, col2 = st.columns(2)

with col1:
    st.info("🎤 Speech Assistant")
    st.write("Convert speech into text and text into speech.")

    st.info("📄 Document Reader")
    st.write("Read and summarize PDF, DOCX and TXT documents.")

with col2:
    st.info("🖼️ Image Understanding")
    st.write("Describe images and extract visible text.")

    st.info("🧭 Voice Navigation")
    st.write("Understand commands and provide application guidance.")

st.markdown("---")
st.caption("AccessMate AI | Student Project Prototype")
