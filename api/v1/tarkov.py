from datetime import datetime, timedelta
import os
from pathlib import Path
import threading
from fastapi import FastAPI, Depends, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from dataprocessor.tasks import TasksDP
from .models import Tasks, TaskDependencies

api = FastAPI()
tasksDP = TasksDP()

origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "http://frontend:3000",
    "http://backend:8000",
]

# Mount the React frontend if the `static` directory exists
static_dir = Path(os.getenv("STATIC_DIR", "/backend/static"))
if static_dir.exists() and static_dir.is_dir():
    api.mount("/static", StaticFiles(directory=static_dir, html=True), name="static")

# In-memory storage for rate limiting
rate_limit_data = {}
RATE_LIMIT = int(os.getenv("RATE_LIMIT", 20))  # Default to 20 requests
RATE_LIMIT_CLEANING_INTERVAL = int(os.getenv("RATE_LIMIT_CLEANING_INTERVAL", 300))  # Default to 5 minutes
TIME_WINDOW = timedelta(seconds=int(os.getenv("TIME_WINDOW", 60)))  # Default to 60 seconds

print(f"RATE_LIMIT: {RATE_LIMIT}, TIME_WINDOW: {TIME_WINDOW}")

def cleanup_rate_limit_data():
    print(f"CLEANING RATE LIMIT DATA: Starting with {len(rate_limit_data.keys())} entries.")
    now = datetime.now()
    for ip in list(rate_limit_data.keys()):
        if now - rate_limit_data[ip]["start_time"] > TIME_WINDOW:
            print(f"----Deleting {ip} from Rate Limit Data")
            del rate_limit_data[ip]
    print(f"FINISHED CLEANING RATE LIMIT DATA: Ended with {len(rate_limit_data.keys())} entries.")

    threading.Timer(RATE_LIMIT_CLEANING_INTERVAL, cleanup_rate_limit_data).start()  # Run cleanup every 60 seconds

# Start cleanup on application startup
@api.on_event("startup")
async def startup():
    cleanup_rate_limit_data()

@api.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    client_ip = request.client.host
    now = datetime.now()

    if client_ip not in rate_limit_data:
        rate_limit_data[client_ip] = {"count": 1, "start_time": now}
    else:
        client_data = rate_limit_data[client_ip]
        if now - client_data["start_time"] > TIME_WINDOW:
            rate_limit_data[client_ip] = {"count": 1, "start_time": now}
        else:
            client_data["count"] += 1
            if client_data["count"] > RATE_LIMIT:
                # Add CORS headers manually
                response = JSONResponse(
                    status_code=429,
                    content={
                        "message": "Rate limit exceeded. Try again later.",
                        "hint": f"Max {RATE_LIMIT} requests per {TIME_WINDOW.seconds // 60} minute(s)."
                    },
                )
                response.headers["Access-Control-Allow-Origin"] = "*"
                response.headers["Access-Control-Allow-Methods"] = "GET"
                response.headers["Access-Control-Allow-Headers"] = "*"
                return response

    response = await call_next(request)
    return response

@api.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == 429:  # Handle rate limit exceptions
        return JSONResponse(
            status_code=429,
            content={
                "message": exc.detail,
                "hint": "You have hit the rate limit. Please wait before making more requests."
            },
        )
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

# Dependency function that returns the processor
def get_dp():
    return tasksDP

# Get all tasks
@api.get("/v1/tasks")
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

@api.get("/{full_path:path}")
async def serve_frontend(full_path: str):
    # Exclude static file requests
    if full_path.startswith("static/") or full_path.startswith("v1/"):
        return {"error": f"Path {full_path} not found."}

    # Serve `index.html` for non-API and non-static paths
    index_file = static_dir / "index.html"
    if index_file.exists():
        return FileResponse(index_file)

    return {"error": "Frontend not found"}
