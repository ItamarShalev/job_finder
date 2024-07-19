import pytest
import os
import sqlite3
from model.candidate import Candidate
from model.interviewer import Interviewer, InterviewerType
from model.position import Position
from model.stage import Stage
from database.database import Department
from pathlib import  Path
# Path to a temporary database file for testing
test_db_file = Path(__file__).parent / 'test.db'

@pytest.fixture(scope='module')
def department():
    # Setup: Create a temporary database
    if os.path.exists(test_db_file):
        os.remove(test_db_file)
    dept = Department(test_db_file)
    yield dept
    # Teardown: Remove the temporary database
    if os.path.exists(test_db_file):
        os.remove(test_db_file)

def test_add_position(department):
    department.add_position("url_1", "Software Engineer", "John Doe", "Tech Corp", "New York", "Job description")
    positions = department.get_all_positions()
    assert len(positions) == 1
    assert positions[0].linkdin_url == "url_1"

def test_add_interviewer(department):
    department.add_interviewer("user1", "password", "Jane Doe", "Tech Corp", "1234567890", "jane@example.com", "HR")
    interviewer = department.get_interviewer_by_user_name("user1")
    assert interviewer.user_name == "user1"

def test_add_stage(department):
    department.add_stage("user1", "Initial interview", 5, "Technical")


def test_add_candidate(department):
    department.add_candidate("Alice", "alice@example.com", "1111111111", "Los Angeles", "Summary", "Keywords", "resume_url", "linkedin_url", "github_url")
    candidate = department.get_candidate_by_phone("1111111111")
    assert candidate.phone == "1111111111"

def test_get_all_positions(department):
    positions = department.get_all_positions()
    assert len(positions) > 0

def test_get_position_by_linkedin_url(department):
    position = department.get_position_by_linkedin_url("url_1")
    assert position.linkdin_url == "url_1"

def test_get_interviewer_by_user_name(department):
    interviewer = department.get_interviewer_by_user_name("user1")
    assert interviewer.user_name == "user1"

def test_get_candidate_by_phone(department):
    candidate = department.get_candidate_by_phone("1111111111")
    assert candidate.phone == "1111111111"

def test_get_candidate_by_position(department):
    candidates = department.get_candidate_by_position("url_1")
    assert len(candidates) > 0

def test_get_candidate_stages(department):
    stages = department.get_candidate_stages("1111111111", "url_1")
    assert len(stages) > 0

def test_get_stage_by_id(department):
    stage = department.get_stage_by_id(1)
    assert stage.id == 1

def test_get_interviewer_type(department):
    department.add_interviewer_type("HR")
    interviewer_type = department.get_interviewer_type("HR")
    assert interviewer_type.interviewer_type == "HR"

# Run the tests
if __name__ == '__main__':
    pytest.main()
