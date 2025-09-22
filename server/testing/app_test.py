import pytest
from app import create_app, db
from models import Restaurant, Pizza, RestaurantPizza
import json

# Fixture to create app for testing
@pytest.fixture
def app_instance():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

# Fixture to get test client
@pytest.fixture
def client(app_instance):
    return app_instance.test_client()


class TestApp:

    def test_restaurants(self, client, app_instance):
        with app_instance.app_context():
            r = Restaurant(name="Test R", address="123 Street")
            db.session.add(r)
            db.session.commit()

            response = client.get("/restaurants")
            data = response.get_json()
            assert response.status_code == 200
            assert len(data) == 1
            assert data[0]["name"] == "Test R"

    def test_restaurants_id(self, client, app_instance):
        with app_instance.app_context():
            r = Restaurant(name="R2", address="456 Avenue")
            db.session.add(r)
            db.session.commit()

            response = client.get(f"/restaurants/{r.id}")
            data = response.get_json()
            assert response.status_code == 200
            assert data["name"] == "R2"

    def test_returns_404_if_no_restaurant_to_get(self, client):
        response = client.get("/restaurants/999")
        data = response.get_json()
        assert response.status_code == 404
        assert data["error"] == "Restaurant not found"

    def test_deletes_restaurant_by_id(self, client, app_instance):
        with app_instance.app_context():
            r = Restaurant(name="ToDelete", address="Nowhere")
            db.session.add(r)
            db.session.commit()
            response = client.delete(f"/restaurants/{r.id}")
            data = response.get_json()
            assert response.status_code == 200
            assert data["message"] == "Restaurant deleted"

    def test_returns_404_if_no_restaurant_to_delete(self, client):
        response = client.delete("/restaurants/999")
        data = response.get_json()
        assert response.status_code == 404
        assert data["error"] == "Restaurant not found"

    def test_pizzas(self, client, app_instance):
        with app_instance.app_context():
            p = Pizza(name="Margherita", ingredients="Cheese, Tomato")
            db.session.add(p)
            db.session.commit()
            response = client.get("/pizzas")
            data = response.get_json()
            assert response.status_code == 200
            assert data[0]["name"] == "Margherita"

    def test_creates_restaurant_pizzas(self, client, app_instance):
        with app_instance.app_context():
            r = Restaurant(name="R3", address="Addr")
            p = Pizza(name="P3", ingredients="Ing")
            db.session.add_all([r, p])
            db.session.commit()

            payload = {"restaurant_id": r.id, "pizza_id": p.id, "price": 15}
            response = client.post("/restaurant_pizzas", json=payload)
            data = response.get_json()
            assert response.status_code == 201
            assert data["price"] == 15

    def test_400_for_validation_error(self, client, app_instance):
        with app_instance.app_context():
            r = Restaurant(name="R4", address="Addr")
            p = Pizza(name="P4", ingredients="Ing")
            db.session.add_all([r, p])
            db.session.commit()

            payload = {"restaurant_id": r.id, "pizza_id": p.id, "price": 50}  # invalid
            response = client.post("/restaurant_pizzas", json=payload)
            data = response.get_json()
            assert response.status_code == 400
            assert "Price must be between 1 and 30" in data["error"]
