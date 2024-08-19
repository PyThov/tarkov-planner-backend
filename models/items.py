from pydantic import BaseModel, HttpUrl
from typing import List, Optional

class Item(BaseModel):
    name: str = ""
    id: str = ""
    image512pxLink: Optional[HttpUrl] = None
    wikiLink: Optional[HttpUrl] = None

# This is essentially an objective, but w/e
class ItemRequirement(BaseModel):
    count: int
    foundInRaid: bool
    items: List[Item]
