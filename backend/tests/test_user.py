from httpx import AsyncClient
import pytest
from backend.app.main import app


@pytest.mark.asyncio
async def test_create_user():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/users/", json={"username": "testuser", "email": "test@email.com", "password": "SicheresPassword"})
    assert response.status_code == 200
    assert response.json()['email'] == "test@example.com"


@pytest.mark.asyncio
async def test_read_user():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/users/testuser")
    assert response.status_code == 200
    assert response.json()['username'] == "testuser"
