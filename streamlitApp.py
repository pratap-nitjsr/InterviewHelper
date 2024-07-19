from src.interviewhelper.utils import read_file
from src.interviewhelper.interviewhelper import generate_evaluate_chain
import streamlit as st
from gtts import gTTS
import os

st.title("Interview Helper")

with st.form("user_input"):
    resume = st.file_uploader("Upload Your Resume (PDF)")

    RESPONSE_JSON = {
        "reply": "Reply for the question"
    }

    question = st.text_input("Enter the question")

    role = st.text_input("Enter Job Role")

    round = st.text_input("Enter type of interview round")

    button = st.form_submit_button("Generate Reply")

    if button and resume is not None and question and role and round:

        with st.spinner("Loading..."):
            try:
                information = read_file(resume)

                response = generate_evaluate_chain({
                    "question": question,
                    "job_role": role,
                    "interview_stage": round,
                    "applicant_info": information
                })

                result = response.get('generated_reply')

                st.markdown(result)

                # Convert text to audio
                tts = gTTS(result)
                audio_file = "response.mp3"
                tts.save(audio_file)

                # Display audio player
                st.audio(audio_file)

                st.balloons()

            except Exception as e:
                st.write(e)
