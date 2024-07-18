from dataclasses import dataclass
from pathlib import PurePosixPath
from typing import Optional, List, Dict

from model.position import Position
from model.stage import Stage


@dataclass
class Candidate:
    name: str
    email: str
    phone: str
    city: str
    summery: str
    bazz_words: List[str]
    stages: Dict[Position, List[Stage]]
    resume_url: PurePosixPath = None
    linkdin_url: Optional[PurePosixPath] = None
    github_url: Optional[PurePosixPath] = None

    def to_json(self):
        stages_json = {}
        for position, stages in self.stages.items():
            stages_json[str(position.linkdin_url)] = [stage.to_json() for stage in stages]
        return {
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "city": self.city,
            "summery": self.summery,
            "bazz_words": self.bazz_words,
            "stages": stages_json,
            "resume_url": str(self.resume_url),
            "linkdin_url": str(self.linkdin_url),
            "github_url": str(self.github_url),
        }

    def __hash__(self):
        return hash(self.phone)

    def __eq__(self, other):
        return self.phone == other.phone
