FROM python:3.11-slim

WORKDIR /app
COPY ./src/ /app

COPY ./pyproject.toml /code/pyproject.toml

RUN apt-get update\
    && apt-get install -y \
        imagemagick \
        ghostscript \
        libreoffice-writer \
        poppler-utils \
        tesseract-ocr \
        tesseract-ocr-ita \
    && apt-get clean
RUN pip install /code/.

EXPOSE 5000
CMD ["bash", "entrypoint.sh"]