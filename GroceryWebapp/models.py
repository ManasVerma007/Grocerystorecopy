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

class Products(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    product_name=db.Column(db.String(150),unique=True,nullable=False)
    manufacture=db.Column(db.String(150))
    expiry=db.Column(db.String(150))
    p_per_u=db.Column(db.Float,nullable=False)
    c_id = db.Column(db.Integer, db.ForeignKey("categories.id") ,nullable = False)
