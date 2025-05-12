from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import io
import base64
from PIL import Image
import pdf2image
import google.generativeai as genai
import pathlib
from pathlib import Path

#path = r"C:\poppler\Library\bin"

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input,pdf_content,prompt):
    model = genai.GenerativeModel('gemini_pro_vision')
    response=model.generate_content([input,pdf_content[0],prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        images=pdf2image.convert_from_bytes(uploaded_file.read())

        first_page=images[0]

        img_byte_arr=io.BytesIO()
        first_page.save(img_byte_arr,format='JPEG')
        
        img_byte_arr=img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type":"image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")
    
## stremlit app
st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")
input_text=st.text_area("Job Description: ",key="input")
uploaded_file =st.file_uploader("Upload your resume(PDF)...",type=["pdf"])

if uploaded_file is not None:
    st.write("pdf uploaded successfully")

submit1= st.button("Tell me About the Resume")

#submit2= st.button("How can I improvise my skills")

submit3=st.button("Percentage match")

input_prompt1 = """
You are an experienced HR with Tech experiance in the field of any one job role Data Science or  Full stack Web Development or Big Data Engineering or  DEVOPS or Data Analyst 
your task is to review the provided resume against the job discription for these profiles.please share your professional eveluation on whether the candidates profile align with
highlight the strength and weakness of the applicant in relation to the specified job requirements"""


input_prompt3 = """
You are skilled ATS (Applicant Tracking system)scanner with a deep understanding of any one job role Data Science or full stack development, DEVOPS Data anlyst and deep ATS functionality.
your task is to review the resume against job discription. Give me the percentage of match First the output should come as percentage and then keywords matching and last final the kiwords missing.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content =input_pdf_setup(uploaded_file)
        response= get_gemini_response(input_prompt1,pdf_content,input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the Resume")

elif submit3:
    if uploaded_file is not None:
        pdf_content =input_pdf_setup(uploaded_file)
        response= get_gemini_response(input_prompt3,pdf_content,input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the Resume")



