from dataclasses import dataclass

from model.interviewer import Interviewer


@dataclass
class Stage:
    reviewer: Interviewer
    summery: str
    score: int
    type: str

    def to_json(self):
        return {
            "reviewer": self.reviewer.to_json(),
            "summery": self.summery,
            "score": self.score,
            "type": self.type,
        }
