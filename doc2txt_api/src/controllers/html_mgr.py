from utils.my_logging import debug
from bs4 import BeautifulSoup as BS, Tag



def _tag_is_page_nav(tag: Tag) -> bool:
    """Check if input tag is a page navigator -> pdfminer HTML output"""
    links = tag.findChildren("a" , recursive=False)

    if links:
        for link in links:
            if link.has_attr('href'):
                return True
    return False


def _tag_has_child(tag: Tag) -> bool:
    """Check if a tag has childs"""
    return len(tag.find_all()) == 0


def _tag_is_empty(tag: Tag) -> bool:
    """Check if tag is empty"""
    if _tag_has_child(tag):
        tag_name = tag.name
        if tag_name == 'div':
            return True
        if tag_name == 'span':
            if len(tag.get_text(strip=True)) == 0:
                return True
    return False


def _unwanted_tag(tag: Tag) -> bool:
    """Check if tag must be extracted from original soup"""
    if _tag_is_page_nav(tag):
        return True
    if _tag_is_empty(tag):
        return True
    return False


def _get_text(soup: BS) -> str:
    text = ""

    text = soup.get_text(separator="").strip()
    text = '\n'.join(' '.join(line.split()) for line in text.split('\n'))
    text = ''.join(c for c in text if c.isprintable() or c == '\n')

    return text


@debug
def process_html(soup: BS) -> str:
    for tag in soup.find_all():
        if _unwanted_tag(tag):
            tag.extract()

    return _get_text(soup)
