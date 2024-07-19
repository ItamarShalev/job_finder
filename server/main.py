from pathlib import Path, PurePosixPath
from tempfile import NamedTemporaryFile

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, Form
import uvicorn
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from database.database import Department
from model.interviewer import Interviewer, InterviewerType
from model.stage import Stage
from model.candidate import Candidate
from model.position import Position
from logic.pdf_reader import PdfReader
from logic.resume_ai import ResumeAI
from logic import linkdin_api

app = FastAPI()

origins = [
    "http://localhost:80",
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
LINKDIN_URL = ""


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
    department = Department()
    candidate = department.get_candidate_by_phone(candidate_phone_number)
    stages = department.get_candidate_stages(candidate.phone, LINKDIN_URL)
    return {"stages": [stage.to_json() for stage in stages]}

@app.post("/api/get_candidates_by_position/")
async def get_candidates_by_position(
    linkdin_url: str = Form(...),
    user_name: str = Form(...)
):
    global LINKDIN_URL
    LINKDIN_URL = linkdin_url
    candidates = Department().get_candidates_by_position(linkdin_url)
    return {"result": [candidate.to_json() for candidate in candidates]}

@app.post("/api/add_linkdin_company/")
async def add_linkdin_company(
    company_linkdin_url: str = Form(...),
    user_name: str = Form(...)
):
    url_lists = []
    if "impreva" in company_linkdin_url.lower():
        url_lists.append("https://www.linkedin.com/jobs/view/3972035392/?alternateChannel=search&refId=d9R%2B5qAx7kqYiJvDYx9XuQ%3D%3D&trackingId=cy7Pnatonja979hQ9ZgW8A%3D%3D")
        url_lists.append("https://www.linkedin.com/jobs/view/3972039029/?alternateChannel=search&refId=d9R%2B5qAx7kqYiJvDYx9XuQ%3D%3D&trackingId=gEd%2F1W6ZdlFjpWfEtf1jaw%3D%3D")
        url_lists.append("https://www.linkedin.com/jobs/view/3972039025/?alternateChannel=search&refId=d9R%2B5qAx7kqYiJvDYx9XuQ%3D%3D&trackingId=mjh4UWcSwMw7gqrDo5oQbA%3D%3D")
        url_lists.append("https://www.linkedin.com/jobs/view/3972039025/?alternateChannel=search&refId=%2FmmydKRt3aIBqnau2vUiJA%3D%3D&trackingId=Vg%2BMUusxlQyvncnHdEYXcA%3D%3D ")
    elif "cellebrite" in company_linkdin_url.lower():
        url_lists.append("https://www.linkedin.com/jobs/view/3973649691/?alternateChannel=search&refId=p0RSKhkgDTvvVh9GseFJ7g%3D%3D&trackingId=8CmIzzpGQ2ow3hzEJGslag%3D%3D")
        url_lists.append("https://www.linkedin.com/jobs/view/3967187784/?alternateChannel=search&refId=p0RSKhkgDTvvVh9GseFJ7g%3D%3D&trackingId=T6byVYPERamxaWwXcZc%2F2g%3D%3D")
        url_lists.append("https://www.linkedin.com/jobs/view/3974873250/?alternateChannel=search&refId=p0RSKhkgDTvvVh9GseFJ7g%3D%3D&trackingId=xU1x6S1YFSdzRRWoswDqHg%3D%3D")
        url_lists.append("https://www.linkedin.com/jobs/view/3977530163/?alternateChannel=search&refId=p0RSKhkgDTvvVh9GseFJ7g%3D%3D&trackingId=wBJ%2BzicmgFHMkDPPMoq%2B%2Bw%3D%3D")
        url_lists.append("https://www.linkedin.com/jobs/view/3690345017/?alternateChannel=search&refId=p0RSKhkgDTvvVh9GseFJ7g%3D%3D&trackingId=APa7VYyqD74G%2FUTqhwIqOA%3D%3D")
    elif "c2a" in company_linkdin_url.lower():
        url_lists.append("https://www.linkedin.com/jobs/view/3972328036/?alternateChannel=search&refId=5OOaWLym8zqs5jcKqjnIHA%3D%3D&trackingId=AlOxkPrPUJXHjbl5iS0BYA%3D%3D")
    else:
        url_lists.append(company_linkdin_url)
    department = Department()
    interviewer = department.get_interviewer_by_user_name(user_name)
    for url in url_lists:
        position = linkdin_api.get_linkedin_job_details(url)
        position.open_by = interviewer.user_name
        department.add_position(position.linkdin_url, position.name, position.open_by, position.company, position.location, position.description)

    positions = department.get_all_positions()
    return {"result": [position.to_json() for position in positions]}

@app.post("/api/create_candidate/")
async def create_candidate(
    pdf_file: UploadFile = File(...),
    positions_selected: str = Form(...)
):
    content = await pdf_file.read()
    with NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(content)
        file_path = Path(temp_file.name)

    resume = ResumeAI(file_path, verbose=False)

    urls = [position for position in positions_selected.split(",")]
    department = Department()
    for index, linkdin_url in enumerate(urls):
        position = Department().get_position_by_linkedin_url(linkdin_url)
        candidate = resume.compute(position)
        if index == 0:
            department.add_candidate(candidate.name, candidate.email, candidate.phone,
                                     candidate.city, candidate.summery, "", str(candidate.resume_url), str(candidate.linkdin_url),
                                     str(candidate.github_url))
        else:
            stage = candidate.stages[position][0]
            department.add_stage(reviewer=stage.reviewer.user_name, summery=stage.summery, score=stage.score, type=stage.type)
    return {"success": True, "message": "Candidate created successfully"}

@app.post("/api/get_positions_by_user_name/")
async def get_positions_by_user_name(
        user_name: str = Form(...)
):
    interview = Department().get_interviewer_by_user_name(user_name)
    positions = Department().get_all_positions()
    return {"result": {"user": interview, "positions": [position.to_json() for position in positions]}}

@app.post("/api/get_position_by_linkdin_url/")
async def get_positions_by_user_name(
        linkdin_url: str = Form(...)
):
    position = Department().get_position_by_linkedin_url(linkdin_url)
    return {"result": position.to_json()}


@app.get("/api/get_positions/")
async def get_positions():
    positions = Department().get_all_positions()
    return {"result": [position.to_json() for position in positions]}

if __name__ == "__main__":
    try:
        Department().add_interviewer("meir", "1234", "Meir Levi", "General HR", "054-1234567", "meir.levi@tech.com",
                                     InterviewerType.HR.name)
    except:
        pass
    uvicorn.run(app, host="0.0.0.0", port=8000)
