import logging

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from config.database import get_mongo_database
from config.logging import config_logger
from config.settings import CORS_ORIGIN_WHITELIST
from repository.factories import get_covid_record_repository
from routes.data_viz_routes import data_viz_router

app = FastAPI(
    title="covid-data-viz-api",
    description="An api for covid data visualization",
    contact={
        "name": "dgop92",
        "url": "https://github.com/dgop92",
    },
)
app.add_middleware(CORSMiddleware, allow_origins=CORS_ORIGIN_WHITELIST)
app.include_router(data_viz_router)


@app.on_event("startup")
def startup():
    config_logger()
    logger = logging.getLogger(__name__)
    logger.info("app started")
    database = get_mongo_database()
    get_covid_record_repository(database)


""" @app.on_event("shutdown")
def shutdown_db_client():
    app.database.close() """
