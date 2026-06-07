from fastapi.testclient import TestClient
from src.main import app


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

def test_get_item_not_found():
    response = client.get("/items/99999")
    assert response.status_code == 404

def test_create_item_missing_name():
    response = client.post("/items", json={"description": "No name"})
    assert response.status_code == 422

def test_get_items_empty():
    response = client.get("/items")
    assert response.json() == []