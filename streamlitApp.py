import streamlit as st
from gtts import gTTS
import base64
import requests
from src.interviewhelper.utils import read_file
from src.interviewhelper.interviewhelper import generate_evaluate_chain
import os

def fetch_transcript():
    try:
        response = requests.get('https://interview-helper-rho.vercel.app/transcript')
        # st.write(response)
        if response.status_code == 200:
            return response.text
        else:
            st.error('Error fetching transcript from server')
            return None
    except Exception as e:
        st.error(f'Error: {e}')
        return None

st.title("Interview Helper")

with st.form("user_input"):
    resume = st.file_uploader("Upload Your Resume (PDF)")

    role = st.text_input("Enter Job Role")

    round = st.text_input("Enter type of interview round")

    question_text = st.text_input("Enter the Question")

    st.markdown("Use Speech-to-Text")

    speech_to_text_html = open("utils/speech_to_text.html", "r").read()
    st.components.v1.html(speech_to_text_html, height=300)

    result_as_text = st.checkbox("Want reply as text also")

    button = st.form_submit_button("Generate Reply")

    if button:
        # Fetch the transcript from the Flask server

        question_audio = None

        try:
            question_audio = fetch_transcript()
        except:
            pass

        # Use the question_text if question_audio is not available
        question = question_audio if question_audio is not None else question_text

        if resume is not None and (question or question_text) and role and round:
            with st.spinner("Loading..."):
                try:
                    # Read the resume file
                    information = read_file(resume)

                    # Generate response using the provided details
                    response = generate_evaluate_chain({
                        "question": question,
                        "job_role": role,
                        "interview_stage": round,
                        "applicant_info": information
                    })

                    result = response.get('generated_reply')

                    # Convert text to audio
                    tts = gTTS(result)
                    audio_file = "response.mp3"
                    tts.save(audio_file)

                    # Display audio player with autoplay
                    audio_html = f"""
                    <audio controls autoplay>
                        <source src="data:audio/mpeg;base64,{base64.b64encode(open(audio_file, "rb").read()).decode()}" type="audio/mpeg">
                        Your browser does not support the audio element.
                    </audio>
                    """
                    st.components.v1.html(audio_html, height=100)

                    if result_as_text:

                        # st.code(result)

                        copy_button_html = f"""
                        <button onclick="navigator.clipboard.writeText('{result}').then(function() {{
                            console.log('Copied to clipboard');
                        }}, function(err) {{
                            console.error('Failed to copy text: ', err);
                        }});">Copy to Clipboard</button>
                        """
                        st.components.v1.html(copy_button_html)
                        
                        st.markdown(result)

                    st.balloons()

                except Exception as e:
                    st.error(f"Error: {e}")

        else:
            st.write("Enter all details")
