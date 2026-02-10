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