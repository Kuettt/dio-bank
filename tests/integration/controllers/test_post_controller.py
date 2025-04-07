from src.app import db, Role

#testar criação de posts com sucesso


def test_create_post(client, access_token):
    role = db.session.execute(db.select(Role.id).where(Role.name == "admin")).scalar()
    payload = {
        "title": "test title",
        "body": "test body" 
    }

    response = client.post("/posts/", json=payload, headers=f"Baerer:{access_token}")

#testar falha na criação de post, por não estar logado.