"""Tests fixtures."""

import pytest
from asgi_lifespan import LifespanManager
from httpx import AsyncClient

from fastapi.testclient import TestClient
from app import app


@pytest.fixture()
def client_test():
    """
    Create an instance of the client.
    :return: yield HTTP client.
    """
    return AsyncClient(app=app, base_url="http://test")
