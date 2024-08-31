"""
Test user route
"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_healthcheck(client_test):
    response = await client_test.get("/healthcheck")
    assert response.status_code == 200
