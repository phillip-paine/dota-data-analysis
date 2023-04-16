"""This file contains the actions for interacting with the database with the api
These are the post and get statements"""
from fastapi import APIRouter, Body, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from .models import TaskModel, UpdateTaskModel

router = APIRouter()


# response_description is used to populate documentation on the api
@router.post("/", response_description="Add new task")
async def create_task(request: Request, task: UpdateTaskModel = Body(...)):
    task = jsonable_encoder(task)  # python dict to json seralised format
    new_task = await request.app.mongodb[''].insert_one(task)  # await allows rest of code to be executed
    # whilst waiting for this connection to db to complete (not fastapi specific command)
    created_task = await request.app.mongodb[''].find_one({'_id': new_task.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_task)


@router.get("/", response_description="List all tasks")
async def list_tasks(request: Request):
    tasks = []
    for doc in await request.app.mongodb[''].find().to_list(length=100):
        tasks.append(doc)
    return tasks


@router.get("/{id}", response_description="Get a task")
async def show_task(id: str, request: Request):
    if (task := await request.app.mongodb.find_one({"_id": id})) is not None:
        # this assignment operator will be set to None if it does not find a document matching string id
        return task

    raise HTTPException(status_code=404, detail=f"Task {id} not found.")


@router.put("/{id}", response_description="Update a task")
async def update_task(id: str, request: Request, task: UpdateTaskModel = Body(...)):
    """we have to pass id because it identifies the task we will update"""
    task = {k: v for k, v in task.dict.items() if v is not None}
    # in UpdatedTaskModel data class we have optional data types - if task only has e.g. name
    # then the 'if v is not None' will ensure we only keep name and not completed. Then when we update
    # the entry in the db we will not overwrite with an empty string
    if len(task) >= 1:
        update_result = await request.app.mongodb[''].update_one({"_id": id, "$set": task})

        # check if the db was successfully updated with new values:
        if update_result.modified_count == 1:
            if (updated_task := await request.app.mongodb[''].find_one({"_id": id})) is not None:
                return updated_task # retrieve and return the updated entry (if it exists)

    if (existing_task := await request.app.mongodb[''].find_one({"_id": id})) is not None:
        return existing_task

    raise HTTPException(status_code=404, detail=f"Task {id} was not found.")


@router.delete("/{id}", response_description="Delete task")
async def delete_task(id: str, request: Request):
    """delete a task from the database"""
    delete_result = await request.app.mongodb[''].delete_one({"_id": id})

    if delete_result.deleted_count == 1:  # check if successfully deleted entry from db
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Task {id} was not found")



