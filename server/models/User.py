from server.util.instances import db
from datetime import datetime as dt
from werkzeug.security import generate_password_hash, check_password_hash
from enum import Enum
from flask_admin.contrib.sqla import ModelView


class User(db.Model):
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
    roles = db.relationship('Role', backref="user_roles", lazy=True)
    def __repr__(self):
        return '%r role' % self.user.name


class RoleAdminView(ModelView):
    form_choices = {'permissions': [(Permissions.READ, "Read"), (Permissions.WRITE, 'Write')]}

class UserAdminView(ModelView):
    
    form_args ={'is_active': dict(description='Check instead of deleting user to deactivate user')}
    column_auto_select_related = True
    column_hide_backrefs = False
    column_exclude_list=('password')
    inline_models = (UserRole,)
    column_labels = {'phone': 'Phone Number', 'is_active': 'Active'}
    column_sortable_list = ('name', 'email', 'username',)
    column_searchable_list = ('name', 'email','username',)
    column_default_sort = [('name',False), ('email',False)]
    column_editable_list = ('name', 'username', 'email',)
    can_delete = False
    
    def on_form_prefill(self, form, id):
        form.password.render_kw = {'readonly': True}

    def on_model_change(self, form, model, is_created):
        if is_created:
            model.password = generate_password_hash(model.password)
    