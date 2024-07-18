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


@app.post("/api/get_stages_by_candidate/")
async def get_stages_by_candidate(
    candidate_phone_number: str = Form(...)
):
    return {[]}

@app.post("/api/get_candidates_by_position/")
async def get_candidates_by_position(
    linkdin_url: str = Form(...),
    user_name: str = Form(...)
):
    return {[]}

@app.post("/api/add_linkdin_company/")
async def add_company_linkdin(
    company_linkdin_url: str = Form(...),
    user_name: str = Form(...)
):
    return {[]}

@app.post("/api/create_candidate/")
async def create_candidate(
    pdf_file: UploadFile = File(...),
    positions_selected: str = Form(...)
):

    return {[]}

@app.post("/api/get_positions_by_user_name/")
async def get_positions_by_user_name(
        user_name: str = Form(...)
):
    return {[]}

@app.get("/api/get_positions/")
async def get_positions():
    return {[]}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
