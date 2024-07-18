from pathlib import Path
from tempfile import NamedTemporaryFile

from fastapi import FastAPI, File, UploadFile, Form
import uvicorn

from logic.pdf_reader import PdfReader

app = FastAPI()


@app.post("/api/demo/")
async def upload_file(
        pdf_file: UploadFile = File(...),
        position_description: str = Form(...)
):
    content = await pdf_file.read()
    with NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(content)
        file_path = Path(temp_file.name)
    print(f"The file saved into: '{file_path}'")
    text = PdfReader(file_path).convert_to_text()
    print(f"pdf reader text: {text}")
    return {"pdf_reader_text": text, "content": str(content), "description": position_description}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
