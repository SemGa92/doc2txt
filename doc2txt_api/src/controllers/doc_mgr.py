import os
import re
from controllers.html_mgr import process_html
from controllers.img_mgr import (
    pdf_to_img,
    img_to_pdf,
    )
from models.document import Document
from utils.my_logging import debug
from bs4 import BeautifulSoup as BS
from pdfminer.high_level import extract_text_to_fp
from pdfminer.layout import LAParams



def _to_pdf(doc: Document) -> Document:
    doc.save_doc()
    if not doc.is_image:
        if doc.extension != '.pdf':
            doc.doc_to_pdf()
    else:
        img_to_pdf(doc.paths['file'], doc.paths['file_pdf'])

    return doc


def _to_html(in_path: str, out_path: str, word_margin: float = 0.4) -> BS:
    """PDF to HTML using pdfminer"""
    with open(in_path, 'rb') as f_in, open(out_path, 'wb') as f_out:
        extract_text_to_fp(
            f_in,
            f_out,
            laparams=LAParams(line_margin=2.0, word_margin=word_margin),
            output_type='html',
            codec="utf-8"
        )

    with open(out_path, 'r', encoding='utf-8') as f:
        soup = BS(f.read(), 'html.parser')

    return soup


def _doc_is_empty(soup: BS) -> bool:
    text = soup.get_text()
    cid = text.count('(cid:')

    if '(cid:' in text:
        text = re.sub(r'\(cid\:\d+\)', '', text)
        text = ' '.join(text.replace('\n', '').split())

    if len(text) < 200:
        return True
    elif len(text) > 200 and cid > 3000:
        return True
    else:
        return False


@debug
def _process_scans(doc: Document) -> str:
    text = ''
    pngs = pdf_to_img(doc.paths['file_pdf'], doc.paths['pngs'])
    for i, png in enumerate(pngs, 1):
        f_out = os.path.join(doc.paths['uid'], f'output-{i}.pdf')
        img_to_pdf(png, f_out)
        soup = _to_html(f_out, f_out.replace('.pdf', '.html'))
        text += process_html(soup)

    return text


@debug
def process_doc(doc: Document) -> str:
    doc = _to_pdf(doc)
    soup = _to_html(doc.paths['file_pdf'], doc.paths['file_html'])

    if _doc_is_empty(soup):
        return _process_scans(doc)
    return process_html(soup)
