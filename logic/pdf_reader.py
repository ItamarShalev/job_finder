from pathlib import Path

import PyPDF2


class PdfReader:

    def __init__(self, pdf_path: Path):
        self.pdf_path = pdf_path
        self._text: str = ""

    def convert_to_text(self) -> str:
        if self._text:
            return self._text
        with open(self.pdf_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text().strip()
        self._text = text.strip()
        return self._text
