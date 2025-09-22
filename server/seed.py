# server/seed.py
from server.models import db, Restaurant, Pizza, RestaurantPizza
from server.app import app

with app.app_context():
    db.drop_all()
    db.create_all()

    r1 = Restaurant(name="Karen's Pizza Shack", address="address1")
    r2 = Restaurant(name="Sanjay's Pizza", address="address2")
    r3 = Restaurant(name="Kiki's Pizza", address="address3")

    p1 = Pizza(name="Emma", ingredients="Dough, Tomato Sauce, Cheese")
    p2 = Pizza(name="Geri", ingredients="Dough, Tomato Sauce, Cheese, Pepperoni")
    p3 = Pizza(name="Melanie", ingredients="Dough, Sauce, Ricotta, Red peppers, Mustard")

    db.session.add_all([r1,r2,r3, p1,p2,p3])
    db.session.commit()

    rp1 = RestaurantPizza(price=10, restaurant_id=r1.id, pizza_id=p1.id)
    rp2 = RestaurantPizza(price=12, restaurant_id=r2.id, pizza_id=p2.id)
    db.session.add_all([rp1, rp2])
    db.session.commit()

    print("seeded")
