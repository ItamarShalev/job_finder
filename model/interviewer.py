from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional, List

from model.position import LinkdinUrl


class InterviewerType(Enum):
    AI = auto()
    HR = auto()
    TL = auto()


@dataclass
class Interviewer:
    type: InterviewerType
    user_name: str
    password: str
    name: str
    company: str
    phone: Optional[str] = None
    email: Optional[str] = None
    positions: List[LinkdinUrl] = field(default_factory=list)

    def __eq__(self, other):
        return self.user_name == other.user_name
