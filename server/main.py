from pathlib import Path, PurePosixPath
from tempfile import NamedTemporaryFile

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, Form
import uvicorn
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from model.interviewer import Interviewer, InterviewerType
from model.stage import Stage
from model.candidate import Candidate
from model.position import Position
from logic.pdf_reader import PdfReader

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    interview1 = Interviewer(type=InterviewerType.AI, user_name="AI", password="password", name="name", company="company", phone="phone", email="email", positions=[PurePosixPath("position")])
    interview2 = Interviewer(type=InterviewerType.HR, user_name="Human Resource", password="password", name="name", company="company", phone="phone", email="email", positions=[PurePosixPath("position")])
    stage1 = Stage(reviewer=interview1, summery="Best worker ever !", score=8, type="First Filter")
    stage2 = Stage(reviewer=interview2, summery="Best worker ever !", score=4, type="First Filter")
    return {"stages": [stage1.to_json(), stage2.to_json()]}

@app.post("/api/get_candidates_by_position/")
async def get_candidates_by_position(
    linkdin_url: str = Form(...),
    user_name: str = Form(...)
):
    candidate = Candidate(name="name", email="email", phone="phone", city="city", summery="summery",
                          bazz_words=["python", "java"], stages={}, resume_url=PurePosixPath("resume"),
                          linkdin_url=PurePosixPath("linkdin_url"), github_url=PurePosixPath("github_url"))
    return {"result": [candidate.to_json() for _ in range(6)]}

@app.post("/api/add_linkdin_company/")
async def add_linkdin_company(
    company_linkdin_url: str = Form(...),
    user_name: str = Form(...)
):
    position = Position(linkdin_url=PurePosixPath("linkdin_url"), name=user_name, open_by="open_by", company="company", location="location", description="description")
    return {"result": [position.to_json() for _ in range(6)]}

@app.post("/api/create_candidate/")
async def create_candidate(
    pdf_file: UploadFile = File(...),
    positions_selected: str = Form(...)
):
    content = await pdf_file.read()
    with NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(content)
        file_path = Path(temp_file.name)

    text = PdfReader(file_path).convert_to_text()
    print(text)
    positions = [PurePosixPath(position) for position in positions_selected.split(",")]
    print(positions)
    return {"success": True, "message": "Candidate created successfully"}

@app.post("/api/get_positions_by_user_name/")
async def get_positions_by_user_name(
        user_name: str = Form(...)
):
    interview = Interviewer(type=InterviewerType.AI, user_name="AI", password="password", name="name", company="company", phone="phone", email="email", positions=[PurePosixPath("position")])
    position = Position(linkdin_url=PurePosixPath("linkdin_url"), name=user_name, open_by="open_by", company="company", location="location", description="description")
    return {"result": {"user": interview, "positions": [position.to_json() for _ in range(3)]}}

@app.post("/api/get_position_by_linkdin_url/")
async def get_positions_by_user_name(
        linkdin_url: str = Form(...)
):
    interview = Interviewer(type=InterviewerType.AI, user_name="AI", password="password", name="name", company="company", phone="phone", email="email", positions=[PurePosixPath("position")])
    position = Position(linkdin_url=PurePosixPath(linkdin_url), name="NAME", open_by="open_by", company="company", location="location", description="description")
    return {"result": position.to_json()}


@app.get("/api/get_positions/")
async def get_positions():
    position = Position(linkdin_url=PurePosixPath("linkdin_url"), name="name", open_by="open_by", company="company", location="location", description="description")
    return {"result": [position.to_json() for _ in range(6)]}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
