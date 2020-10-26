from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
jwt = JWTManager()

def initializeDB(app):
    db.init_app(app)


def initializeJWT(app):
    jwt.init_app(app)