# FILEPATH: /c:/Users/Jaime/Documents/Python/mi-proyecto-fastapi/tests/test_example_route.py
from fastapi.testclient import TestClient
from main import app
from app.schemas import ExampleSchema

client = TestClient(app)

def test_get_example():
    response = client.get("/example")
    assert response.status_code == 200
    assert response.json() == {"message": "Este es un ejemplo"}