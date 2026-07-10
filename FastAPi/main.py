from typing import List, Optional
from fastapi import FastAPI, HTTPException, status, Response, Depends
from pydantic import BaseModel, EmailStr, Field

app = FastAPI()

# --- Pydantic Models ---
class Task(BaseModel):
    id: str
    title: str
    completed: bool

class TaskCreate(BaseModel):
    title: str
    completed: Optional[bool] = False

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    completed: Optional[bool] = None

# --- In-Memory Database ---
task_db = [
    Task(id="1", title="Buy groceries", completed=False),
    Task(id="2", title="Finish project report", completed=True),
    Task(id="3", title="Call the bank", completed=False),
]

# --- Endpoints ---

@app.get("/")
def root():
    return {"root": "App is running"}

# GET all  --- TESTED
@app.get("/task", status_code=status.HTTP_200_OK, response_model=List[Task])
async def get_all_tasks(
    completed: bool | None = None 
):
    if completed:
        complete = [x for x in task_db if x.completed == True]
        return complete
    return task_db

# GET a single task by ID --- TESTED
@app.get("/task/{task_id}", status_code=status.HTTP_200_OK, response_model=Task)
async def get_task_by_id(task_id: str):
    for task in task_db:
        if task.id == task_id:
            return task
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"Task with id {task_id} not found"
    )

# POST a new task   --- TESTED
@app.post("/task", status_code=status.HTTP_201_CREATED, response_model=Task)
async def create_task(task_input: TaskCreate):
    new_id = str(len(task_db) + 1)
    new_task = Task(id=new_id, title=task_input.title, completed=task_input.completed)
    task_db.append(new_task)
    return new_task

# PATCH / Update an existing task    
@app.patch("/task/{task_id}", status_code=status.HTTP_200_OK, response_model=Task)
async def update_task(task_id: str, task_update: TaskUpdate):
    for task in task_db:
        if task.id == task_id:
            if task_update.title is not None:
                task.title = task_update.title
            if task_update.completed is not None:
                task.completed = task_update.completed
            return task
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"Task with id {task_id} not found"
    )

# DELETE a task
@app.delete("/task/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: str):
    for index, task in enumerate(task_db):
        if task.id == task_id:
            task_db.pop(index)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"Task with id {task_id} not found"
    )
