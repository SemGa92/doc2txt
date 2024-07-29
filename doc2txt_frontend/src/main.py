import os
import base64
import json
import jwt
import requests
import time
import streamlit as st

DOC2TXT_URL = os.getenv("DOC2TXT_URL")

def get_token():
    now = int(time.time())
    to_encode = {
        "nbf" : now, # NOT BEFORE - WHEN THIS TOKEN IS CONSIDERED VALID
        "exp" : now + 1800, # EXPIRY - 1/2 HR (1800 SECS) FROM NOW IN THIS EXAMPLE
    }
    return jwt.encode(to_encode, os.getenv('JWT_KEY'), algorithm='HS512')



with st.sidebar:
    st.header("About")
    st.markdown(
        """
        DOC2TXT is a converter of generic document format to txt.\n
        Behind the scenes, DOC2TXT uses [LibreOffice](https://www.libreoffice.org/)
        and [Tesseract](https://tesseract-ocr.github.io/) to manage input formats
        and - for this reason - it supports the formats accepted by the two softwares.\n
        You can currently load: pdf, doc, docx, odt, rtf, jpg, png.
        """
    )

st.title("Generic document To TXT Converter")
st.info("Hi :smile: Need some help converting a document to text? :rocket:")



uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    if st.button('Send file'):
        headers = {
        'Authorization': f'Bearer {get_token()}',
        'Content-type': 'application/json'
        }

        payload = {
            'source': 'locale',
            'f_name': uploaded_file.name,
            "content": base64.b64encode(uploaded_file.getvalue()).decode("utf-8")
            }
        response = requests.post(DOC2TXT_URL, data=json.dumps(payload), headers=headers, verify=False)
        try:
            st.text(response.json()['text'])
        except KeyError:
            st.text(response.json()['error'])
