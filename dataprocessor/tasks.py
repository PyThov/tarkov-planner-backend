from models.tasks import Tasks, Task
from models.items import ItemRequirement
from adapters.tarkov import TarkovAPI
from utils.utils import time_something
from typing import List, Dict, Optional

class TasksDP:
    def __init__(self, data: Tasks | None = None) -> None:
        self.tarkovAPI = TarkovAPI()
        if data is None:
            print("NO DATA: Getting task data")
            newData, _ = self.tarkovAPI.get_tasks()
            self.data = newData
        else:
            print("Already have data.")
            self.data = data

    @time_something
    def find_task_from_id(self, id: str) -> Task:
        for task in self.data.tasks:
            if task.id == id:
                print(f"found task {id}")
                return task
        print(f"could not find task {id}")
        return Task()
    
    @time_something
    def get_all_tasks(self) -> List[Task]:
        return self.data.tasks
    
    # Function to find all task dependencies using Pydantic models and Python typing
    @time_something
    def get_task_dependencies(self, task: Task) -> tuple[List[Task], List[ItemRequirement]]:
        # Create a dictionary for quick lookup of tasks by ID
        task_dict: Dict[str, Task] = {task.id: task for task in self.data.tasks}
        
        tasks: List[Task] = []
        itemReqs: List[ItemRequirement] = []
        visited: set = set()
        
        # depth first search
        def dfs(current_task_id: str, itemReqs:  List[ItemRequirement] = []):
            if current_task_id in visited:
                return
            visited.add(current_task_id)
            
            current_task: Task = task_dict[current_task_id]
            
            for requirement in current_task.taskRequirements:
                required_task_name: str = requirement.task['name']
                # Find the required task by name (assuming names are unique)
                required_task: Optional[Task] = next((t for t in self.data.tasks if t.name == required_task_name), None)
                if required_task:
                    dfs(required_task.id)
            
            # After visiting all dependencies, add the current task to the tasks
            tasks.append(current_task)
            return self._get_items_from_task(current_task, itemReqs)

        # Start the DFS from the given task
        itemReqs = dfs(task.id)
        
        # Return the tasks in the order required to complete the given task
        return tasks, itemReqs

    # Get a list of required items for the given task
    def _get_items_from_task(self, task: Task, itemReqs: List[ItemRequirement] = []) -> List[ItemRequirement]:
        # Loop through each objective in the task.
        for obj in task.objectives:
            # Check if the objective type is "giveItem" (meaning it requires giving an item).
            if obj.type == "giveItem":
                # Loop through each item in the objective's items list.
                for item in obj.items:
                    # Try to find if the item already exists in the itemReqs list.
                    existingItem = next(filter(lambda newItem: newItem.name == item.name, itemReqs), None)
                    
                    # If the item does not exist in the list, create a new ItemRequirement and add it.
                    if existingItem is None:
                        itemReqs.append(ItemRequirement(
                            count=obj.count,              # The required quantity of the item.
                            foundInRaid=obj.foundInRaid,  # Whether the item must be found in a raid.
                            id=item.id,                   # The unique ID of the item.
                            image512pxLink=item.image512pxLink,  # The URL of the item's image.
                            name=item.name,               # The name of the item.
                            wikiLink=item.wikiLink,       # The URL link to the item's wiki page.
                        ))
                    else:
                        # If the item already exists in the list, update the count by adding the new objective's count.
                        existingItem.count += obj.count

        # Return the list of item requirements.
        return itemReqs

    @staticmethod
    def get_min_lvl_from_tasks(tasks: List[Task]) -> int:
        return max(tasks, key=lambda task: task.minPlayerLevel).minPlayerLevel
    
    @staticmethod
    def count_items_req(itemReqs: List[ItemRequirement]) -> int:
        return sum(item.count for item in itemReqs )
