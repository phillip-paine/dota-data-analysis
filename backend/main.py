import uvicorn  # this is an asychronous gateway server interface - hence use it with fastapi
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from backend.apps.app.routers import router as app_router
from config import settings

app = FastAPI()


@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(settings.DB_URL)
    app.mongodb = app.mongodb_client(settings.DB_URL)
    # we set the database as an attribute of the fastapi app for use within application handlers


@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()


app.include_router(app_router, tags=["tasks"], prefix="/task")
# the prefix would be added to all endpoints

if __name__ == '__main__':
    uvicorn.run("main:app", host=settings.HOST, reload=settings.DEBUG_MODE, port=settings.PORT)