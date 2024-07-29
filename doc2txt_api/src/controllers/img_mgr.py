import os
import pytesseract as pyt
from utils.my_logging import debug
from PIL import Image as PImage
from pdf2image import convert_from_path
from wand.image import Image
from wand.color import Color



def _img_resize(img: Image) -> Image:
    max_w = 1600

    width = img.width
    if width > max_w:
        factor = (max_w*100)/img.width
        new_h = int((img.height*factor)/100)
        img.sample(max_w, new_h)

    return img


def _img_features(img: Image, fmt: str) -> Image:
    img.format = fmt
    img.background_color = Color('white')
    img.alpha_channel = 'remove'
    img.depth = 8

    return img


def _img_processing(img: Image, i: int, fmt: str, dir_out: str) -> None:
    img = _img_resize(img)
    img = _img_features(img, fmt)
    _ = _img_save(img, i, dir_out)


def _img_save(img: Image|PImage.Image, i: int, dir_out: str) -> str:
    output = os.path.join(dir_out, f'output-{i}.png')
    if isinstance(img, Image):
        img.save(filename=output)
    elif isinstance(img, PImage.Image):
        img.save(output)

    return output


@debug
def img_to_pdf(f_in: str, f_out: str) -> None:
    pdf = pyt.image_to_pdf_or_hocr(
        f_in,
        lang='ita',
        nice=1,
        extension='pdf',
        )

    with open(f_out, 'wb') as f:
        f.write(pdf)


@debug
def pdf_to_img(f_path: str, dir_out: str) -> list[str]:
    os.mkdir(dir_out)

    res = 300
    fmt = 'png'

    pages = convert_from_path(pdf_path=f_path, dpi=res, fmt=fmt)
    pngs = [_img_save(page, i, dir_out) for i, page in enumerate(pages, 1)]

    for i, page in enumerate(pngs, 1):
         with Image(filename=page, resolution=res) as img:
             _img_processing(img, i, fmt, dir_out)

    return pngs