import json
import os
import requests
from .constants import TARKOV_ENDPOINT, PATHS
from .queries import ALL_TASKS
from utils.utils import time_something
from models.tasks import Tasks

class TarkovAPI:
    tasksPath = PATHS["tasks"]

    def __init__(self) -> None:
        pass

    @time_something
    def get_tasks(self) -> Tasks:
        if os.path.exists(self.tasksPath):
            print(f"File {self.tasksPath} exists; reading existing data.")
            with open(self.tasksPath, "r", encoding='utf-8') as file:
                data = json.load(file)
                data = dict(data).get("data")
                tasks = Tasks(tasks=dict(data).get("tasks"))
            return tasks
        else:
            print(f"File {self.tasksPath} does not exist; fetching data.")
            return self._fetch_tasks()

    def _fetch_tasks(self) -> Tasks:
        res = self._run_query(ALL_TASKS)
        data = dict(res)
        if data.get("errors"):
            for err in data["errors"]:
                print(err["message"])
            return res

        with open(self.tasksPath, "w") as file:
            json.dump(data, file)

        return Tasks(tasks=data.get("data", []))

    def _run_query(self, query: str):
        headers = {"Content-Type": "application/json"}
        response = requests.post(TARKOV_ENDPOINT, headers=headers, json={'query': query})
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Query failed to run by returning code of {}. {}".format(response.status_code, query))
