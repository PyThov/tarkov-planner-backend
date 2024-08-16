from fastapi import FastAPI, Depends, Query
from dataprocessor.tasks import TasksDP
from .models import Tasks, TaskDependencies

api = FastAPI()
tasksDP = TasksDP()

# Dependency function that returns the processor
def get_dp():
    return tasksDP

# Get all tasks
@api.get("/tasks")
def get_tasks(offset: int = Query(0), limit: int = Query(10), tdp: TasksDP = Depends(get_dp)):
    items, time = tdp.get_all_tasks()
    tasks = Tasks(tasks=items[offset:offset+limit], count=limit, offset=offset, total=len(items))
    print(f"Took {time} to get /tasks")

    return tasks

# Get a single task from task id
@api.get("/tasks/{task_id}")
def get_task(task_id: str, tdp: TasksDP = Depends(get_dp)):
    task, time = tdp.find_task_from_id(task_id)
    print(f"Took {time} to get /tasks/{task_id}")

    return task

# Get the 'plan' for a task
@api.get("/task_plan/{task_id}")
def get_task_plan(task_id: str, tdp: TasksDP = Depends(get_dp)):
    task, time = tdp.find_task_from_id(task_id)
    [tasks, itemReqs], newTime = tdp.get_task_dependencies(task)
    time += newTime

    print(f"Took {time} to get dependencies for {task_id}")

    data = TaskDependencies(
        tasks=tasks,
        items=itemReqs,
        levelRequired=tdp.get_min_lvl_from_tasks(tasks),
        tasksTotal=len(tasks),
        itemsTotal=tdp.count_items_req(itemReqs)
        )

    return data
