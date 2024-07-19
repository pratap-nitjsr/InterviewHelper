import streamlit as st
from gtts import gTTS
import os
import base64
from src.interviewhelper.utils import read_file
from src.interviewhelper.interviewhelper import generate_evaluate_chain
from utils.HelperFunctions import get_audio_ques

st.title("Interview Helper")

with st.form("user_input"):
    resume = st.file_uploader("Upload Your Resume (PDF)")

    role = st.text_input("Enter Job Role")

    round = st.text_input("Enter type of interview round")

    question_text = st.text_input("Enter the Question")

    st.markdown("Use Speech-to-Text")

    speech_to_text_html = open("utils/speech_to_text.html", "r").read()
    st.components.v1.html(speech_to_text_html, height=300)

    question_audio = get_audio_ques(speech_to_text_html)

    result_as_text = st.checkbox("Want reply as text also")

    button = st.form_submit_button("Generate Reply")

    if button and resume is not None and (question_audio or question_text) and role and round:
        with st.spinner("Loading..."):
            try:
                information = read_file(resume)

                question = question_audio if question_audio else question_text

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
                    st.markdown(result)

                st.balloons()

            except Exception as e:
                st.error(f"Error: {e}")

    elif button:
        st.write("Enter all details")
