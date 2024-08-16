from pydantic import BaseModel, HttpUrl
from typing import Dict, List, Optional
from models.objectives import Objective

class Map(BaseModel):
    name: str

class Trader(BaseModel):
    name: str
    imageLink: HttpUrl

class TaskRequirementTask(BaseModel):
    name: str

class TaskRequirement(BaseModel):
    task: Dict[str, str]

class Task(BaseModel):
    id: str = ''
    name: str = ''
    trader: Optional[Trader] = None # Assuming Trader has a valid default or is optional
    map: Optional[Map] = None
    wikiLink: Optional[HttpUrl] = None
    taskImageLink: Optional[HttpUrl] = None
    minPlayerLevel: int = 0
    taskRequirements: List[TaskRequirement] = []
    objectives: List[Objective] = []

class Tasks(BaseModel):
    tasks: List[Task]
