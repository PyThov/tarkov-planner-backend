from adapters.tarkov import TarkovAPI
from dataprocessor.tasks import TasksDP
from utils.utils import *

# TODO: Integrate completed tasks into planning

def main():
    tasksDP = TasksDP()
    # items = tasksDP.get_all_tasks()
    # print(items)
    # task, _ = tasksDP.find_task_from_id("657315ddab5a49b71f098853")
    task, _ = tasksDP.find_task_from_id("59ca2eb686f77445a80ed049")
    # print(task)
    deps = tasksDP.get_task_dependencies(task)
    # print(deps)
    # print(task.objectives)
    for obj in task.objectives:
        print(obj.description)
        print(obj.count)
        print(obj.type)
        for item in obj.items:
            print(item.name)
        print()
    
    

main()
