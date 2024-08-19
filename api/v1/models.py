from pydantic import BaseModel
from typing import List
from models.tasks import Task
from models.items import ItemRequirement

# REQUESTS
# ===============================================================


# RESPONSES
# ===============================================================
class Tasks(BaseModel):
    tasks: List[Task]
    total: int
    count: int
    offset: int

class TaskDependencies(BaseModel):
    name: str
    tasks: List[Task]
    items: List[ItemRequirement]
    itemsTotal: int
    tasksTotal: int
    levelRequired: int

# A single Task response is just the normal Task model