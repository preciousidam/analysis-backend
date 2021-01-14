from server.util.instances import db
from datetime import datetime as dt
from werkzeug.security import generate_password_hash, check_password_hash
from enum import Enum
from flask_admin.contrib.sqla import ModelView
from secrets import token_urlsafe
from .Auth import Auth


class User(db.Model, Auth):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(14), nullable=True)
    password = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean())
    created_at = db.Column(db.DateTime(timezone=True), default=dt.now())
    updated_at = db.Column(db.DateTime(timezone=True), default=dt.now(), onupdate=dt.now())


    def __repr__(self):
        return 'User %r' % self.username

    def get_id(self):
        return self.id

    # Required for administrative interface
    def __unicode__(self):
        return self.username
    
    def json(self):
        return {
            'id': self.id,
            'username': self.username,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }

    def hashPassword(self, password):
        self.password = generate_password_hash(password)

    def checkPassword(self, password):
        return check_password_hash(self.password, password)

    
class ResetToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    token = db.Column(db.String(255), nullable=False, default=token_urlsafe(16))
    created_at = db.Column(db.DateTime(timezone=True), default=dt.now())
    updated_at = db.Column(db.DateTime(timezone=True), default=dt.now(), onupdate=dt.now())

    def __repr__(self):
        return 'Reset token for %r' % self.email

    def updateToken(self):
        self.token = token_urlsafe(16)

    def get_token(self):
        return self.token
    
    def json(self):
        return {
            'email': self.email,
            'token': self.name,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }

class Permissions(Enum):
    READ = 'read'
    WRITE = 'write'

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(15), nullable=False)
    permissions = db.Column(db.String(255), db.Enum(Permissions), default=Permissions.READ, nullable=False)
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


class UserRole(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))
    user = db.relationship('User', backref="user_roles", lazy=False)
    role = db.relationship('Role', backref="user_roles", lazy=True)
    def __repr__(self):
        return '%r role' % self.user.name

    def json(self):
        return {
            'id': self.id,
            'user': self.user_id,
            'role': self.role.title,
            'permissions': self.role.permissions,
        }