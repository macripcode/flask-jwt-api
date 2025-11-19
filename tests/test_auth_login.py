import pytest
from models.user import User
from extensions import db

# ------------------------------------
# Helper: crear usuario de prueba
# ------------------------------------
def create_test_user(email="test@example.com", password="123456"):
    user = User(email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user


# ------------------------------------
# TEST 1: email requerido
# ------------------------------------
def test_login_missing_email(client):
    response = client.post("/auth/login", json={
        "password": "123456"
    })
    assert response.status_code == 400
    assert response.get_json()["msg"] == "email required"


# ------------------------------------
# TEST 2: usuario inexistente
# ------------------------------------
def test_login_user_not_found(client):
    response = client.post("/auth/login", json={
        "email": "notfound@example.com",
        "password": "whatever"
    })
    assert response.status_code == 401
    assert response.get_json()["msg"] == "Bad credentials"


# ------------------------------------
# TEST 3: contraseña incorrecta
# ------------------------------------
def test_login_wrong_password(client):
    create_test_user(email="cami@example.com", password="abcdef")

    response = client.post("/auth/login", json={
        "email": "cami@example.com",
        "password": "wrongpass"
    })

    assert response.status_code == 401
    assert response.get_json()["msg"] == "Bad credentials"


# ------------------------------------
# TEST 4: login correcto (JWT devuelto)
# ------------------------------------
def test_login_success(client):
    create_test_user(email="macripco@example.com", password="mypass")

    response = client.post("/auth/login", json={
        "email": "macripco@example.com",
        "password": "mypass"
    })

    data = response.get_json()

    assert response.status_code == 200
    assert "access_token" in data
    assert isinstance(data["access_token"], str)
