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

    def __eq__(self, other):
        return self.linkdin_url == other.linkdin_url
