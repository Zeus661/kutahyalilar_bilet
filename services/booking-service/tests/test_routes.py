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
    assert response.json()["service"] == "booking-service"


@pytest.mark.asyncio
async def test_create_booking_requires_auth(client):
    response = await client.post(
        "/api/v1/bookings/",
        json={
            "trip_id": "00000000-0000-0000-0000-000000000000",
            "seat_id": "00000000-0000-0000-0000-000000000000",
            "passenger_name": "Test",
            "passenger_tc": "12345678901",
            "passenger_gender": "male",
            "passenger_dob": "1990-01-01"
        }
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_list_my_bookings_requires_auth(client):
    response = await client.get("/api/v1/bookings/my")
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_all_bookings_requires_admin(client):
    response = await client.get("/api/v1/bookings/")
    assert response.status_code == 403
