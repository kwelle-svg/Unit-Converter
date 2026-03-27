import pytest
from httpx import AsyncClient
from fastapi.testclient import TestClient
from app.main import app, convert_unit

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200

def test_converter():
    pass