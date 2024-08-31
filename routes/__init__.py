from fastapi import FastAPI
from .v1.account import router as account_router


def init_router(app: FastAPI):
    """
    Initialise the FastAPI router with all existing routers
    :param app: app to initialise
    :return: None - Include router of app
    """

    app.include_router(account_router)
