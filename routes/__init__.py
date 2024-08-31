from fastapi import FastAPI


def init_router(app: FastAPI):
    """
    Initialise the FastAPI router with all existing routers
    :param app: app to initialise
    :return: None - Include router of app
    """
