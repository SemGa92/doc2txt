class AccessDenied(Exception):
    """JWT auth failed"""
    def __init__(self, message: str) -> None:
        super().__init__(message)


class LibreOfficeConversion(Exception):
    """Raised when libreoffice failed pdf conversion"""
    def __init__(self, ext: str) -> None:
        msg = f"LibreOffice is not able to convert the document to pdf format.\
            Extension: {ext}"
        super().__init__(msg)