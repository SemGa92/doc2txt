# doc2txt
## Flask API + Streamlit Web App
DOC2TXT is a converter of generic document format to txt.\
Behind the scenes, DOC2TXT uses [LibreOffice](https://www.libreoffice.org/)
and [Tesseract](https://tesseract-ocr.github.io/) to manage input formats
and - for this reason - it supports the formats accepted by the two softwares.\
You can currently load: pdf, doc, docx, odt, rtf, jpg, png.

## How to use it
Clone this repo and then run
```bash
cd doc2txt
docker compose up --build
# or
# docker-compose up --build
# depending on your local compose configuration.
```
Browse to http://localhost:8501 to use the web app.\
If you don't need the web app
```bash
cd doc2txt
docker compose up doc2txt_api --build
# or
# docker-compose up doc2txt_api --build
# depending on your local compose configuration.
```
Refer to the [request](https://github.com/SemGa92/doc2txt/blob/main/tests/request.py) file to make your first request.\
Make sure to edit f_name variable - line 30 - with the full path of your document.