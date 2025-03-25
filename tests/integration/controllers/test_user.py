from http import HTTPStatus
from src.app import User, Role, db


def test_get_user_success(client):

    role = Role(name="admin")
    db.session.add(role)
    db.session.commit()

    user = User(username="test", password="test", role_id=role.id)
    db.session.add(user)
    db.session.commit()

    response = client.get(f'/users/{user.id}')
    assert response.status_code == HTTPStatus.OK
    assert response.json == [{'active': user.active, 'id': user.id, 'name': user.username}]



def test_get_user_not_found(client):
    role = Role(name="admin")
    db.session.add(role)
    db.session.commit()

    user = User(username="John-Doe", password="test", role_id=role.id)

    response = client.get(f"/users/{user.id}")
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json == None