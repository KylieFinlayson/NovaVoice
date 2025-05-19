import streamlit as st
import whisper
import tempfile
import os

st.set_page_config(page_title="NovaVoice: Voice-to-Process + User Stories", layout="wide")
st.title("🎙️ NovaVoice: Voice-to-Process + User Stories")

model = whisper.load_model("base")

# Placeholder user story generation
def generate_user_story(step_text):
    return f"As a user, I want to {step_text.lower()}, so that I achieve my goal."

def generate_acceptance_criteria(step_text):
    return [
        f"Given the system is ready,",
        f"When {step_text.lower()},",
        f"Then the expected outcome should occur."
    ]

uploaded_file = st.file_uploader("Upload an audio file (.mp3 or .wav)", type=["mp3", "wav"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    st.info("Transcribing...")
    result = model.transcribe(tmp_path)
    st.success("Transcription complete!")

    st.markdown("### 📝 Transcript")
    st.text_area("Transcript:", result["text"], height=300)

    st.markdown("### 🔄 Process Steps + 📋 User Stories")
    steps = [s.strip() for s in result["text"].split(".") if len(s.strip()) > 5]
    user_stories = []

    for i, step in enumerate(steps):
        st.markdown(f"**Step {i+1}:** {step}")
        story = generate_user_story(step)
        ac = generate_acceptance_criteria(step)
        st.markdown(f"📋 **User Story:** {story}")
        st.markdown("✅ **Acceptance Criteria:**")
        for line in ac:
            st.markdown(f"- {line}")
        user_stories.append(story)

    if st.button("Download User Stories (.txt)"):
        with open("user_stories.txt", "w", encoding="utf-8") as f:
            for story in user_stories:
                f.write(story + "\n")
        st.success("User stories saved as user_stories.txt!")