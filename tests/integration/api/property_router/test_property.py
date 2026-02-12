import pytest
from fastapi.testclient import TestClient
from app.core.config import settings


@pytest.mark.integration
def test_create_property_success(client: TestClient, test_env_logged):
    
    payload = {
        "description": "Apartamento incrível",
        "price": 100000.00,
        "private_area": 60.00,
        "address": {
            "zip_code": "90020000",
            "country": "BR",
            "state": "RS",
            "city": "Porto Alegre",
            "neighborhood": "Centro",
            "street": "Rua das Flores",
            "number": "100",
            "complement": "101",
            "latitude": -30.0,
            "longitude": -51.0,
        }
    }

    response = client.post(f"{settings.API_PREFIX}/properties/", json=payload)

    assert response.status_code in (200, 201)    
    data = response.json()

    assert data["description"] == "Apartamento incrível"
    assert data["price"] == "100000.00"
    assert data["private_area"] == "60.00"
    assert data["address"]["zip_code"] == "90020000"
    assert data["address"]["country"] == "BR"
    assert data["address"]["state"] == "RS"
    assert data["address"]["city"] == "Porto Alegre"
    assert data["address"]["neighborhood"] == "Centro"
    assert data["address"]["street"] == "Rua das Flores"
    assert data["address"]["number"] == "100"
    assert data["address"]["complement"] == "101"
    assert data["address"]["latitude"] == "-30.000000"
    assert data["address"]["longitude"] == "-51.000000"


    assert "public_id" in data
    assert "profile_public_id" in data






# def test_list_properties_empty(client, db):
#     response = client.get("/properties")

#     assert response.status_code == 200

#     data = response.json()
#     assert isinstance(data,list)
#     assert data == []

# def test_create_property(client):
#     from tests.factories.property_factory import property_payload_factory

#     payload = property_payload_factory()

#     response = client.post("/properties", json=payload)

#     assert response.status_code == 200

#     data = response.json()
#     assert "id" in data
#     assert data["description"] == payload["description"]
#     assert data["price"] == payload["price"]


# def test_list_properties_returns_created_property(client):
#     from tests.factories.property_factory import property_payload_factory

#     payload = property_payload_factory(description="Casa")

#     client.post("/properties", json=payload)
#     response = client.get("/properties")

#     assert response.status_code == 200
#     data = response.json()

#     assert any(p["description"] == "Casa" for p in data)