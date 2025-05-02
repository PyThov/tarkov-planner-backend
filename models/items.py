from pydantic import BaseModel, HttpUrl, validator
from typing import List, Optional

class Item(BaseModel):
    name: str = ""
    id: str = ""
    image512pxLink: Optional[HttpUrl] = None
    wikiLink: Optional[HttpUrl] = None

    @validator('image512pxLink', 'wikiLink', pre=True)
    def empty_string_to_none(cls, v):
        if v == "":
            return None
        return v

# This is essentially an objective, but w/e
class ItemRequirement(BaseModel):
    count: int
    foundInRaid: bool
    items: List[Item]
