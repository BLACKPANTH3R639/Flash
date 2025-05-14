
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
import uuid

router = APIRouter()
agents = {}
tasks = {}
results = []

class RegisterRequest(BaseModel):
    hostname: str
    username: str
    os: str

class RegisterResponse(BaseModel):
    agent_id: str

class Task(BaseModel):
    task_id: str
    command: str

class ResultSubmission(BaseModel):
    agent_id: str
    task_id: str
    result: str

@router.post("/register", response_model=RegisterResponse)
def register(agent: RegisterRequest):
    agent_id = str(uuid.uuid4())
    agents[agent_id] = {
        "info": agent,
        "tasks": []
    }
    return {"agent_id": agent_id}

@router.get("/tasks/{agent_id}", response_model=List[Task])
def get_tasks(agent_id: str):
    if agent_id not in agents:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agents[agent_id]["tasks"]

@router.post("/results")
def submit_result(data: ResultSubmission):
    if data.agent_id not in agents:
        raise HTTPException(status_code=404, detail="Agent not found")
    results.append({
        "agent_id": data.agent_id,
        "task_id": data.task_id,
        "result": data.result
    })
    return {"status": "ok"}

@router.post("/tasks/{agent_id}/add")
def add_task(agent_id: str, task: Task):
    if agent_id not in agents:
        raise HTTPException(status_code=404, detail="Agent not found")
    agents[agent_id]["tasks"].append(task)
    return {"status": "task added"}

@router.get("/results")
def get_results():
    return results
