from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail


mail = Mail()
db = SQLAlchemy()
jwt = JWTManager()


def initializeDB(app):
    db.init_app(app)


def initializeJWT(app):
    jwt.init_app(app)

def initializeMail(app):
    mail.init_app(app) 
