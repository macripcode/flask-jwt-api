import pytest
from models.product import Product
from models.user import User
from extensions import db
from flask_jwt_extended import create_access_token


# ---------------------------------
# Helper: create test user + token
# ---------------------------------
def create_user_and_token(app, email="test@example.com", password="123456"):
    with app.app_context():
        user = User(email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        token = create_access_token(identity=str(user.id))
        return token


# ---------------------------------
# Helper: create product
# ---------------------------------
def create_product(name="Laptop", price=999.99, stock=10):
    p = Product(name=name, price=price, stock=stock)
    db.session.add(p)
    db.session.commit()
    return p


# ---------------------------------
# TEST 1: Cannot access without JWT
# ---------------------------------
def test_products_requires_jwt(client):
    resp = client.get("/products")
    assert resp.status_code == 401


# ---------------------------------
# TEST 2: List products
# ---------------------------------
def test_list_products(client, app):
    token = create_user_and_token(app)

    # Insert sample products
    create_product("Mouse", 20.5, 50)
    create_product("Keyboard", 45.0, 30)

    resp = client.get(
        "/products",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert resp.headers["X-Total-Count"] == "2"


# ---------------------------------
# TEST 3: Get one product
# ---------------------------------
def test_get_single_product(client, app):
    token = create_user_and_token(app)
    p = create_product("Monitor", 150.0, 5)

    resp = client.get(
        f"/products/{p.id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert resp.status_code == 200
    data = resp.get_json()
    assert data["id"] == p.id
    assert data["name"] == "Monitor"


# ---------------------------------
# TEST 4: Create product (success)
# ---------------------------------
def test_create_product(client, app):
    token = create_user_and_token(app)

    resp = client.post(
        "/products",
        json={"name": "Tablet", "price": 250.0, "stock": 3},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert resp.status_code == 201
    data = resp.get_json()
    assert data["name"] == "Tablet"
    assert data["price"] == 250.0
    assert data["stock"] == 3


# ---------------------------------
# TEST 5: Create product (missing fields)
# ---------------------------------
def test_create_product_missing_fields(client, app):
    token = create_user_and_token(app)

    resp = client.post(
        "/products",
        json={"price": 30},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert resp.status_code == 400
    assert resp.get_json()["msg"] == "name and price are required"


# ---------------------------------
# TEST 6: Update product
# ---------------------------------
def test_update_product(client, app):
    token = create_user_and_token(app)
    p = create_product("Old Name", 10, 1)

    resp = client.put(
        f"/products/{p.id}",
        json={"name": "New Name", "price": 20.5},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert resp.status_code == 200
    data = resp.get_json()
    assert data["name"] == "New Name"
    assert data["price"] == 20.5


# ---------------------------------
# TEST 7: Delete product
# ---------------------------------
def test_delete_product(client, app):
    token = create_user_and_token(app)
    p = create_product()

    resp = client.delete(
        f"/products/{p.id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert resp.status_code == 200
    assert resp.get_json()["deleted"] == p.id

    # Ensure product no longer exists
    with app.app_context():
        assert Product.query.get(p.id) is None
