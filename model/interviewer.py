from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, List

from model.position import LinkdinUrl


class InterviewerType(Enum):
    AI = "AI"
    HR = "HR"
    TL = "TL"


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

    def to_json(self):
        return {
            "type": self.type.value,
            "user_name": self.user_name,
            "password": self.password,
            "name": self.name,
            "company": self.company,
            "phone": self.phone,
            "email": self.email,
            "positions": [str(position) for position in self.positions],
        }

    def __hash__(self):
        return hash(self.user_name)

    def __eq__(self, other):
        return self.user_name == other.user_name
