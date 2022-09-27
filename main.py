import logging

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from config.logging import config_logger
from config.settings import CORS_ORIGIN_WHITELIST
from routes.data_viz_routes import data_viz_router

app = FastAPI(
    title="covid-data-viz-api",
    description="An api for covid data visualization",
    contact={
        "name": "dgop92",
        "url": "https://github.com/dgop92",
    },
)

config_logger()


app.add_middleware(CORSMiddleware, allow_origins=CORS_ORIGIN_WHITELIST)

app.include_router(data_viz_router)


@app.on_event("startup")
def on_startup():
    logger = logging.getLogger(__name__)
    logger.info("app started")
