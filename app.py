from config.config import Settings
from fastapi.middleware.cors import CORSMiddleware
from fastapi_versioning import VersionedFastAPI
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
import asyncio
from config.config import Settings
import os

from database.mongod import init_db
from routes import init_router


async def start_up():
    print("Starting up the app")
    await init_db()


def init_app():

    app_ = FastAPI(
        title=Settings().APP_NAME,
        version=Settings().APP_VERSION,
        description=Settings().APP_DESCRIPTION,

    )

    # Await the async init_db function
    init_router(app_)

    app_ = VersionedFastAPI(
        app_, enable_latest=True, version_format="{major}", prefix_format="/v{major}"
    )

    app_.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )

    @app_.get("/healthcheck", status_code=200)
    def api_healthcheck():
        return "OK 200 - app running successfully"

    app_.add_event_handler("startup", start_up)


    return app_


# # register routers
# app.include_router(course.router)


app = init_app()
