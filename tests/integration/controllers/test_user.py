import pytest
from http import HTTPStatus
from sqlalchemy import func
from src.app import User, Role, db



def test_create_user(client, access_token):

    role_id = db.session.execute(db.select(Role.id).where(Role.name == "admin")).scalar()
    payload = {
        "username": "user2", 
        "password": "user2",
        "role_id": role_id
    }


    response = client.post("/users/", json=payload, headers={"Authorization": f"Bearer {access_token}"})

    assert response.status_code == HTTPStatus.CREATED
    assert response.json == {"message": "User created"}, HTTPStatus.CREATED
    assert db.session.query(func.count(User.id)).scalar() == 2


def test_get_user_success(client, access_token):

    user = db.session.execute(db.select(User).where(User.id == 1)).scalar()
    response = client.get(f'/users/{user.id}')
    
    assert response.status_code == HTTPStatus.OK
    assert response.json == [{'active': user.active, 'id': user.id, 'name': user.username}]

def test_get_user_failure(client, access_token):
    role = Role(name="admin")
    db.session.add(role)
    db.session.commit()
    user = User(username="John Doe", password="test", role_id=role.id)
    db.session.add(user)

    results = client.get(f"/users/{user.id}")

    assert results.status_code == HTTPStatus.NOT_FOUND
    assert results.json is None
    
def test_list_users(client, access_token):
    #given

    user = db.session.execute(db.select(User).where(User.id == 1)).scalar()
    role = db.session.execute(db.select(Role).where(Role.name == "admin")).scalar()

    response = client.post('/auth/login', json={'username': user.username, 'password': user.password})
    access_token = response.json['access_token']

    #When
    response = client.get(f"/users/", headers={"Authorization": f'Bearer {access_token}'})

    #Then
    assert response.status_code == HTTPStatus.OK
    assert response.json ==  {'user': [{'id': user.id, 'role': {'id': user.role_id, 'name': role.name}, 'username': user.username}]}
