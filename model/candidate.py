from dataclasses import dataclass
from pathlib import PurePosixPath
from typing import Optional, List, Dict

from position import Position
from stage import Stage


@dataclass
class Candidate:
    name: str
    email: str
    phone: str
    summery: str
    bazz_words: List[str]
    stages: Dict[Position, List[Stage]]
    resume_url: PurePosixPath = None
    linkdin_url: Optional[PurePosixPath] = None
    github_url: Optional[PurePosixPath] = None

    def __eq__(self, other):
        return self.phone == other.phone
