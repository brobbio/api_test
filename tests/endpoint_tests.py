from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_item():
    response = client.post(
        "/items",
        json={
            "name": "Keyboard",
            "description": "Mechanical keyboard"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Keyboard"
    assert data["description"] == "Mechanical keyboard"
    assert "id" in data

def test_get_items():
    response = client.get("/items")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    

def test_create_and_retrieve_item():
    create_response = client.post(
        "/items",
        json={
            "name": "Mouse",
            "description": "Wireless"
        }
    )

    assert create_response.status_code == 201


    item_id = create_response.json()["id"]

    get_response = client.get(f"/items/{item_id}")

    assert get_response.status_code == 200
    assert get_response.json()["id"] == item_id