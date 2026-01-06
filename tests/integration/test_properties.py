def test_list_properties_empty(client, db):
    response = client.get("/properties")

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data,list)
    assert data == []