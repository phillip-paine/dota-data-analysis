"""This file contains the actions for interacting with the database with the api
These are the post and get statements"""
from fastapi import APIRouter, Body, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from .models import TaskModel, UpdateTaskModel

router = APIRouter()


@router.post("/", response_description="Add new task")
async def create_task(request: Request, task: UpdateTaskModel = Body(...)):



@router.get("/", response_description="List all tasks")
async def list_tasks(request: Request):



@router.get("/{id}", response_description="Get a task")
async def show_task(request: Request):



@router.put("/{id}", response_description="Update a task")
async def update_task(id: str, request: Request, task: UpdateTaskModel = Body(...)):
    """we have to pass id because it identifies the task we will update"""







