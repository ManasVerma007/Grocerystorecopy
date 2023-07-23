from . import db # importing current package (website folder) ie: db object
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model,UserMixin):  # schema of the user sign-up info
    id =db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(150),unique=True)
    password=db.Column(db.String(150))
    first_name=db.Column(db.String(150))
    Place=db.Column(db.String(150))

class Categories(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    cat_name=db.Column(db.String(150),unique=True,nullable=False)
    products = db.relationship('Products', backref='category')

class Products(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    product_name=db.Column(db.String(150),unique=True,nullable=False)
    manufacture=db.Column(db.String(150))
    expiry=db.Column(db.String(150))
    p_per_u=db.Column(db.Float,nullable=False)
    c_id = db.Column(db.Integer, db.ForeignKey("categories.id") ,nullable = False)

class Cart(db.Model,UserMixin):
    cart_id=db.Column(db.Integer,primary_key=True)
    cart_item_id=db.Column(db.Integer,db.ForeignKey("products.id"),nullable=False)
    cart_user_id=db.Column(db.Integer,db.ForeignKey("user.id"),nullable = False)
    cart_cat_id = db.Column(db.Integer, db.ForeignKey("categories.id") ,nullable = False)
    cart_quantity=db.Column(db.Integer,nullable=False)
    cart_amount=db.Column(db.Float,nullable=False)
    product = db.relationship('Products', foreign_keys=[cart_item_id])
    Categs = db.relationship('Categories', foreign_keys=[cart_cat_id])
