from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from server.models.User import Role, User, UserAdminView, RoleAdminView
from server.models.Properties import Property, Price, PropertyAdmin
from server.util.instances import db

admin = Admin(template_mode='bootstrap3')

def initializeAdmin(app):
    admin.init_app(app)
    admin.add_view(UserAdminView(User, db.session))
    admin.add_view(RoleAdminView(Role, db.session))
    admin.add_view(PropertyAdmin(Property, db.session))