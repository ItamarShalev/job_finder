from pathlib import Path

from logic.pdf_reader import PdfReader


class TestPdfReader:

    TEST_PDF_PATH = Path(__file__).parent / "test_pdf_contains_hello_world.pdf"

    def test_convert_pdf(self):
        pdf_reader = PdfReader(self.TEST_PDF_PATH)
        text = pdf_reader.convert_to_text()
        assert text == "hello_world"
