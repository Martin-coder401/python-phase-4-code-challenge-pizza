from app import db

class Pizza(db.Model):
    __tablename__ = "pizzas"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    ingredients = db.Column(db.String(200), nullable=False)

class Restaurant(db.Model):
    __tablename__ = "restaurants"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)

class RestaurantPizza(db.Model):
    __tablename__ = "restaurant_pizzas"
    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'), nullable=False)
    _price = db.Column("price", db.Integer, nullable=False)

    # Price validation (1–30)
    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if not (1 <= value <= 30):
            raise ValueError("Price must be between 1 and 30")
        self._price = value

    # Relationships
    restaurant = db.relationship('Restaurant', backref=db.backref('restaurant_pizzas', lazy=True))
    pizza = db.relationship('Pizza', backref=db.backref('restaurant_pizzas', lazy=True))
