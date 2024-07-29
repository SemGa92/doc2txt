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
        Lorem ipsum dolor sit amet, consectetur adipiscing elit.
        Donec cursus leo orci, vitae ultricies diam interdum ut. Nulla facilisi.
        Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos.
        Praesent ac molestie turpis, at placerat ligula. Sed at arcu accumsan, ullamcorper magna vel, maximus arcu. Duis eget venenatis odio.
        Suspendisse eu lectus a magna sodales congue. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas.
        Suspendisse tempor nisi ipsum, in hendrerit urna condimentum sed.
        Pellentesque luctus blandit interdum. Aliquam bibendum nisi sit amet diam congue semper.
        Donec at lacus eget est vulputate gravida. Nunc ac aliquet odio, eu finibus dolor.
        Maecenas tincidunt lectus urna, non faucibus risus tempor id.
        """
    )

st.title("Document To TXT Converter")
st.info("I accept all formats supported by Libreoffice or Tesseract")



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
