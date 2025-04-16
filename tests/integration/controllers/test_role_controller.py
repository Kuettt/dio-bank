from http import HTTPStatus


def test_create_role(client):    
    response = client.post("/roles/", json={"name": "admin"})

    assert response.status_code == HTTPStatus.CREATED
    assert response.json == {'message': 'role created'}, HTTPStatus.CREATED

