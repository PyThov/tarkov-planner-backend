from pydantic import BaseModel, HttpUrl
from typing import Optional

class Item(BaseModel):
    name: str = ""
    id: str = ""
    image512pxLink: Optional[HttpUrl] = None
    wikiLink: Optional[HttpUrl] = None

class ItemRequirement(Item):
    count: int
    foundInRaid: bool
