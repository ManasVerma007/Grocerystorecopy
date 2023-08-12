from . import db  # Importing current package (website folder), i.e., the db object
from flask_login import UserMixin


# User model representing user sign-up information
class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)  # Primary key for the user
    email = db.Column(db.String(150), unique=True)  # User's email address
    password = db.Column(db.String(150))  # User's password
    first_name = db.Column(db.String(150))  # User's first name
    Place = db.Column(db.String(150))  # User's place of residence


# Categories model representing product categories
class Categories(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)  # Primary key for the category
    cat_name = db.Column(db.String(150), unique=True, nullable=False)  # Category name
    products = db.relationship(
        "Products", backref="category"
    )  # Relationship with Products model


# Products model representing individual products
class Products(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)  # Primary key for the product
    product_name = db.Column(
        db.String(150), nullable=False
    )  # Product name
    manufacture = db.Column(db.String(150))  # Manufacturing date of the product
    expiry = db.Column(db.String(150))  # Expiry date of the product
    p_per_u = db.Column(db.Float, nullable=False)  # Price per unit of the product
    stock = db.Column(db.Integer, nullable=False)  # Available stock quantity
    c_id = db.Column(
        db.Integer, db.ForeignKey("categories.id"), nullable=False
    )  # Category foreign key


# Cart model representing user's shopping cart
class Cart(db.Model, UserMixin):
    cart_id = db.Column(db.Integer, primary_key=True)  # Primary key for the cart
    cart_item_id = db.Column(
        db.Integer, db.ForeignKey("products.id"), nullable=False
    )  # Product foreign key
    cart_user_id = db.Column(
        db.Integer, db.ForeignKey("user.id"), nullable=False
    )  # User foreign key
    cart_cat_id = db.Column(
        db.Integer, db.ForeignKey("categories.id"), nullable=False
    )  # Category foreign key
    cart_quantity = db.Column(
        db.Integer, nullable=False
    )  # Quantity of the product in the cart
    cart_amount = db.Column(
        db.Float, nullable=False
    )  # Total amount of the product in the cart
    product = db.relationship(
        "Products", foreign_keys=[cart_item_id]
    )  # Relationship with Products model
    Categs = db.relationship(
        "Categories", foreign_keys=[cart_cat_id]
    )  # Relationship with Categories model
