import pytest
from httpx import AsyncClient, ASGITransport


@pytest.fixture
async def client():
    from app.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_health(client):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["service"] == "trip-service"


@pytest.mark.asyncio
async def test_create_route_admin_only(client):
    response = await client.post(
        "/api/v1/routes/",
        json={"origin": "Kütahya", "destination": "İstanbul", "distance_km": 350, "estimated_duration_min": 300}
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_list_routes_requires_auth(client):
    response = await client.get("/api/v1/routes/")
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_search_trips_requires_auth(client):
    response = await client.get("/api/v1/trips/search?origin=Kütahya&destination=İstanbul&date=2025-01-01")
    assert response.status_code == 403
