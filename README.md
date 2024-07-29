# doc2txt
Converter of generic document format to txt.\
Behind the scenes, doc2txt uses Libreoffice and Tesseract to manage input formats and - for this reason - it supports all formats accepted by the two softwares.

## How to use it
Clone this repo and then run
```bash
cd doc2txt
docker-compose up --build
```
Browse to http://localhost:8501 to use the web app.