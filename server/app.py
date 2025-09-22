from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

# 1. Define db first
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pizza.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Import models after db is initialized
    from models import Pizza, Restaurant, RestaurantPizza

    # Create tables if they don't exist
    with app.app_context():
        db.create_all()

    # ---- Routes ----

    # Get all restaurants
    @app.route('/restaurants', methods=['GET'])
    def get_restaurants():
        restaurants = Restaurant.query.all()
        return jsonify([{"id": r.id, "name": r.name, "address": r.address} for r in restaurants])

    # Get restaurant by ID
    @app.route('/restaurants/<int:id>', methods=['GET'])
    def get_restaurant(id):
        restaurant = Restaurant.query.get(id)
        if restaurant:
            return jsonify({"id": restaurant.id, "name": restaurant.name, "address": restaurant.address})
        return jsonify({"error": "Restaurant not found"}), 404

    # Delete restaurant by ID
    @app.route('/restaurants/<int:id>', methods=['DELETE'])
    def delete_restaurant(id):
        restaurant = Restaurant.query.get(id)
        if restaurant:
            db.session.delete(restaurant)
            db.session.commit()
            return jsonify({"message": "Restaurant deleted"})
        return jsonify({"error": "Restaurant not found"}), 404

    # Get all pizzas
    @app.route('/pizzas', methods=['GET'])
    def get_pizzas():
        pizzas = Pizza.query.all()
        return jsonify([{"id": p.id, "name": p.name, "ingredients": p.ingredients} for p in pizzas])

    # Create a restaurant_pizza
    @app.route('/restaurant_pizzas', methods=['POST'])
    def create_restaurant_pizza():
        data = request.get_json()
        try:
            rp = RestaurantPizza(
                restaurant_id=data['restaurant_id'],
                pizza_id=data['pizza_id'],
                price=data['price']
            )
            db.session.add(rp)
            db.session.commit()
            return jsonify({"id": rp.id, "restaurant_id": rp.restaurant_id, "pizza_id": rp.pizza_id, "price": rp.price}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 400

    return app


# Optional: allow running via `python app.py`
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
