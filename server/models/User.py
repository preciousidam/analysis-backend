from server.util.instances import db
from datetime import datetime as dt
from werkzeug.security import generate_password_hash, check_password_hash
from enum import Enum

class User(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(14), nullable=True)
    role = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=dt.now())
    updated_at = db.Column(db.DateTime(timezone=True), default=dt.now(), onupdate=dt.now())


    def __repr__(self):
        return 'User %r' % self.username

    
    def json(self):
        return {
            'id': self.id,
            'username': self.username,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'role': self.role,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }

    def hashPassword(self, password):
        self.password = generate_password_hash(password)

    def checkPassword(self, password):
        return check_password_hash(self.password, password)

class Permissions(Enum):
    READ = 'read'
    WRITE = 'write'

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(15), nullable=False)
    permissions = db.Column(db.String(255), db.Enum(Permissions), default=Permissions.READ, nullable=False)
    users = db.relationship('User', backref='roles', lazy=False)
    created_at = db.Column(db.DateTime(timezone=True), default=dt.now())
    updated_at = db.Column(db.DateTime(timezone=True), default=dt.now(), onupdate=dt.now())

    def __repr__(self):
        return '%r role' % self.title

    
    def json(self):
        return {
            'id': self.id,
            'role': self.title,
            'permissions': self.permissions,
        }