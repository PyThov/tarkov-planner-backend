See the UI here: https://github.com/PyThov/tarkov-planner-ui

# Tarkov Planner - Backend

To run the API:
```bash
python -m uvicorn api.v1.tarkov:api --reload
```


A Python service to process and serve tarkov API data to plan your tasks!

API Needs:
 - Get list of tasks
    - Name
    - ID
    - Image
    - Description
    - Requirements
    - Map
 <!-- - Get specific task info
    - Name
    - ID
    - Image
    - Description
    - Requirements
    - Map -->
 - Get path for task
    - Required tasks before selected one
    - Total required items
    - Required level for last task
