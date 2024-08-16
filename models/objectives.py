from pydantic import BaseModel
from typing import List
from models.items import Item

class Objective(BaseModel):
    description: str = ""
    id: str = ""
    count: int = 0
    foundInRaid: bool = False
    items: List[Item] = []
    type: str = ""
