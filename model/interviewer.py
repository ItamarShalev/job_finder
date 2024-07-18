from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional, List

from position import LinkdinUrl


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
    phone: Optional[str]
    email: Optional[str]
    positions: List[LinkdinUrl]

    def __eq__(self, other):
        return self.user_name == other.user_name
