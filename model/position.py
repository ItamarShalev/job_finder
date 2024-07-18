from dataclasses import dataclass
from pathlib import PurePosixPath

LinkdinUrl = PurePosixPath
UserName = str


@dataclass
class Position:
    linkdin_url: LinkdinUrl
    name: str
    open_by: UserName
    company: str
    location: str
    description: str

    def to_json(self):
        return {
            "linkdin_url": str(self.linkdin_url),
            "name": self.name,
            "open_by": self.open_by,
            "company": self.company,
            "location": self.location,
            "description": self.description
        }

    def __hash__(self):
        return hash(self.linkdin_url)

    def __eq__(self, other):
        return self.linkdin_url == other.linkdin_url
