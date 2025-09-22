import pytest
from app import create_app, db
from models import RestaurantPizza, Restaurant, Pizza

@pytest.fixture
def app_instance():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

class TestRestaurantPizza:

    def test_price_between_1_and_30(self, app_instance):
        with app_instance.app_context():
            r = Restaurant(name="R", address="Addr")
            p = Pizza(name="P", ingredients="I")
            db.session.add_all([r, p])
            db.session.commit()

            rp = RestaurantPizza(restaurant_id=r.id, pizza_id=p.id, price=10)
            db.session.add(rp)
            db.session.commit()
            assert rp.price == 10

    def test_price_too_low(self, app_instance):
        with app_instance.app_context():
            r = Restaurant(name="R", address="Addr")
            p = Pizza(name="P", ingredients="I")
            db.session.add_all([r, p])
            db.session.commit()

            import pytest
            with pytest.raises(ValueError):
                RestaurantPizza(restaurant_id=r.id, pizza_id=p.id, price=0)

    def test_price_too_high(self, app_instance):
        with app_instance.app_context():
            r = Restaurant(name="R", address="Addr")
            p = Pizza(name="P", ingredients="I")
            db.session.add_all([r, p])
            db.session.commit()

            import pytest
            with pytest.raises(ValueError):
                RestaurantPizza(restaurant_id=r.id, pizza_id=p.id, price=31)
