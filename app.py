import streamlit as st
import os
import time
import google.generativeai as genai
from pypdf import PdfReader

# Retrieve the API keys from the environment variables
GEMINI_API_KEY = os.environ["GOOGLE_API_KEY"]
genai.configure(api_key=GEMINI_API_KEY)

st.write("Hougang Factory :sunglasses: Testing Gemini 1.5 Pro :sunglasses:")

gemini = genai.GenerativeModel('gemini-1.5-pro-latest')

instruction = st.text_input("Customise your own unique prompt:", "Generate short summaries of the articles. Present the summary of each article as one concise and coherent paragraph.")

uploaded_files = st.file_uploader("**Upload** the PDF documents to analyse:", type = "pdf", accept_multiple_files = True)
count = 0
input_text = ""
for uploaded_file in uploaded_files:
  raw_text = ""
  if uploaded_file is not None:
    count = count + 1
    raw_text = raw_text = "### Start of Article " + str(count) + "###\n\n"
    doc_reader = PdfReader(uploaded_file)
    for i, page in enumerate(doc_reader.pages):
      text = page.extract_text()
      if text:
        raw_text = raw_text + text + "\n"
    raw_text = raw_text = "### End of Article " + str(count) + "###\n\n"
  input_text = input_text + raw_text
  
with st.spinner("Running AI Model..."):
  start = time.time()
  prompt = "Read the text below." + instruction + "\n\n" + input_text
  response = gemini.generate_content(prompt)
  answer = response.text
  st.write(response.prompt_feedback)  
  end = time.time()
  st.write(answer)
  st.write("Time to generate: " + str(round(end-start,2)) + " seconds")
  
