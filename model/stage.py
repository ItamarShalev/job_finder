from dataclasses import dataclass

from model.interviewer import Interviewer


@dataclass
class Stage:
    reviewer: Interviewer
    summery: str
    score: int
    type: str
