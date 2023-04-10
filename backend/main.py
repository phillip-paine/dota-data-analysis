import uvicorn  # this is an asychronous gateway server interface - hence use it with fastapi
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from .config import settings

app = FastAPI()

@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(settings.DB_URL)
    app.mongodb = app.mongodb_client(settings.DB_URL)
    # we set the database as an attribute of the fastapi app for use within application handlers


@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()


if __name__ == '__main__':
    uvicorn.run()