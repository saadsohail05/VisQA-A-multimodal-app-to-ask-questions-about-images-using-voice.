import streamlit as st
from st_audiorec import st_audiorec
import os
from PIL import Image
import qa
import asr
import tts

# Create a directory for temporary files if it doesn't exist
TEMP_DIR = "temp_files"
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)

def save_uploaded_file(uploaded_file, dir_path):
    """Saves an uploaded file to a specified directory."""
    if uploaded_file is not None:
        file_path = os.path.join(dir_path, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return file_path
    return None

st.set_page_config(layout="wide", page_title="VisQA App")
st.title("VisQA: Ask Questions About Images Using Voice")

# Initialize session state variables
if 'transcribed_text' not in st.session_state:
    st.session_state.transcribed_text = ""
if 'qa_answer' not in st.session_state:
    st.session_state.qa_answer = ""
if 'audio_answer_path' not in st.session_state:
    st.session_state.audio_answer_path = ""
if 'image_path' not in st.session_state:
    st.session_state.image_path = ""
if 'temp_audio_path' not in st.session_state:
    st.session_state.temp_audio_path = "" # To store path of recorded audio

col1, col2 = st.columns(2)

# Changed order: Image upload first
with col1:
    st.header("1. Upload Image")
    uploaded_image_file = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg"], key="image_uploader")

    if uploaded_image_file:
        # Save uploaded image to a temporary file
        st.session_state.image_path = save_uploaded_file(uploaded_image_file, TEMP_DIR)
        if st.session_state.image_path:
            try:
                image = Image.open(st.session_state.image_path)
                st.image(image, caption="Uploaded Image.", use_column_width=True)
                st.success("Image uploaded successfully! Now you can record your question.")
            except Exception as e:
                st.error(f"Error displaying image: {e}")
                st.session_state.image_path = "" # Reset if error
        else:
            st.session_state.image_path = "" # Reset if save failed
    elif st.session_state.image_path and os.path.exists(st.session_state.image_path):
        # If no new file is uploaded but an old one exists in session state, display it
        try:
            image = Image.open(st.session_state.image_path)
            st.image(image, caption="Uploaded Image.", use_column_width=True)
            st.success("Image ready! Now you can record your question.")
        except FileNotFoundError:
             st.warning("Previously uploaded image not found. Please upload again.")
             st.session_state.image_path = ""
        except Exception as e: # Catch other PIL errors
            st.error(f"Error re-displaying image: {e}")
            st.session_state.image_path = ""
    else:
        st.warning("Please upload an image first before recording your question.")

with col2:
    st.header("2. Record Your Question")
    
    # Check if image is uploaded before allowing recording
    image_uploaded = st.session_state.image_path and os.path.exists(st.session_state.image_path)
    
    if not image_uploaded:
        st.warning("Please upload an image first (in step 1).")
        placeholder_for_recorder = st.empty()
        placeholder_for_recorder.info("Audio recording will be enabled after uploading an image.")
    else:
        # Record audio. User controls duration (implicitly up to a reasonable limit for a question)
        audio_bytes = st_audiorec()

        if audio_bytes: # Check if data is returned
            # Display recorded audio
            st.audio(audio_bytes, format="audio/wav")
            
            # Save recorded audio to a temporary file
            st.session_state.temp_audio_path = os.path.join(TEMP_DIR, "recorded_audio.wav")
            with open(st.session_state.temp_audio_path, "wb") as f:
                f.write(audio_bytes)
            
            try:
                with st.spinner("Transcribing audio..."):
                    # asr.transcribe_audio expects a file path
                    transcription_result = asr.transcribe_audio(st.session_state.temp_audio_path)
                    # Assuming transcription_result has a .text attribute based on common patterns
                    st.session_state.transcribed_text = transcription_result.text 
                    st.success("Transcription complete!")
            except AttributeError: # If .text attribute is not found
                 st.error("Transcription result format error. Expected a '.text' attribute.")
                 st.session_state.transcribed_text = "Error: Could not parse transcription."
            except Exception as e:
                st.error(f"Error during transcription: {e}")
                st.session_state.transcribed_text = "Error in transcription."

        # Text area for transcribed question, allowing edits
        st.text_area(
            "Transcribed Question (edit if needed):", 
            value=st.session_state.transcribed_text,
            height=100,
            key="transcribed_text_area",
            on_change=lambda: setattr(st.session_state, 'transcribed_text', st.session_state.transcribed_text_area)
        )

st.markdown("---")
st.header("3. Get Answer")

# Determine if the "Ask Question" button should be disabled
ask_button_disabled = not (st.session_state.image_path and \
                           os.path.exists(st.session_state.image_path) and \
                           st.session_state.transcribed_text and \
                           st.session_state.transcribed_text.strip() != "" and \
                           st.session_state.transcribed_text != "Error in transcription." and \
                           st.session_state.transcribed_text != "Error: Could not parse transcription.")


if st.button("Ask Question", disabled=ask_button_disabled, key="ask_button"):
    if st.session_state.image_path and os.path.exists(st.session_state.image_path) and \
       st.session_state.transcribed_text and st.session_state.transcribed_text.strip():
        try:
            with st.spinner("Thinking... Getting answer from VLM..."):
                st.session_state.qa_answer = qa.answer_question(st.session_state.image_path, st.session_state.transcribed_text)
            st.success("Answer received!")
            
            with st.spinner("Preparing audio for the answer..."):
                audio_output_filename = os.path.join(TEMP_DIR, "answer_audio.mp3")
                tts.text_to_speech(st.session_state.qa_answer, filename=audio_output_filename)
                st.session_state.audio_answer_path = audio_output_filename
            st.success("Audio for answer is ready!")

        except Exception as e:
            st.error(f"Error in QA process: {e}")
            st.session_state.qa_answer = f"Sorry, an error occurred: {e}"
            st.session_state.audio_answer_path = ""
    else:
        st.warning("Please ensure you have a valid transcribed question and an uploaded image.")

if st.session_state.qa_answer:
    st.subheader("Answer:")
    st.markdown(st.session_state.qa_answer) # Use markdown for better formatting if answer contains it
    if st.session_state.audio_answer_path and os.path.exists(st.session_state.audio_answer_path):
        try:
            with open(st.session_state.audio_answer_path, "rb") as audio_file:
                audio_bytes_answer = audio_file.read()
            st.audio(audio_bytes_answer, format="audio/mp3")
        except Exception as e:
            st.error(f"Could not load or play answer audio: {e}")

st.markdown("---")
st.info("Instructions: 1. Upload an image. 2. Record your question about the image. 3. Click 'Ask Question'.")