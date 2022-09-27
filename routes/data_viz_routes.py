from fastapi import APIRouter

data_viz_router = APIRouter()


@data_viz_router.get("/")
async def index():
    return {"message": "Hello World!"}
