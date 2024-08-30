from fastapi import FastAPI, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from dataprocessor.tasks import TasksDP
from .models import Tasks, TaskDependencies

api = FastAPI()
tasksDP = TasksDP()

origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "http://frontend:3000",
]

api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Dependency function that returns the processor
def get_dp():
    return tasksDP

# Get all tasks
@api.get(f"/v1/tasks")
def get_tasks(offset: int = Query(0), limit: int = Query(default=10), searchTerm: str = Query(""), tdp: TasksDP = Depends(get_dp)):
    if len(searchTerm) > 0:
        items, time = tdp.filter_tasks_by_name(searchTerm)
    else:
        items, time = tdp.get_all_tasks()

    tasks = Tasks(tasks=items[offset:offset+limit], count=limit, offset=offset, total=len(items))

    print(f"Took {time} to get /tasks")

    return tasks

# Get a single task from task id
@api.get("/v1/tasks/{task_id}")
def get_task(task_id: str, tdp: TasksDP = Depends(get_dp)):
    task, time = tdp.find_task_from_id(task_id)
    print(f"Took {time} to get /tasks/{task_id}")

    return task

# Get the 'plan' for a task
@api.get("/v1/task_plan/{task_id}")
def get_task_plan(task_id: str, tdp: TasksDP = Depends(get_dp)):
    task, time = tdp.find_task_from_id(task_id)
    [tasks, itemReqs], newTime = tdp.get_task_dependencies(task)
    time += newTime

    print(f"Took {time} to get dependencies for {task_id}")

    data = TaskDependencies(
        name=task.name,
        tasks=tasks,
        items=itemReqs,
        levelRequired=tdp.get_min_lvl_from_tasks(tasks),
        tasksTotal=len(tasks),
        itemsTotal=tdp.count_items_req(tasks)
        )

    return data
