from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user


db = SQLAlchemy()
DB_NAME = "database.db" # name of the database is given here

def create_database(app):
    if not path.exists('GroceryWebapp/' + DB_NAME):
        db.create_all(app=app)


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'ghosty'

    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' # data is being stored in the loaction given in the f string in the website folder
    db.init_app(app)     # initialize the database by providing the flask app 



    from .models import User #function -->(models.py file runs before we create the database)
    with app.app_context():
     db.create_all()

    from .main import main
    from .auth import auth
    app.register_blueprint(main, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def loader_user(id):
        return User.query.get((id))

    return app
