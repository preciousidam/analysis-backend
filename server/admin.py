from flask import url_for, redirect, request, render_template, flash
from flask_admin import AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, LoginManager, logout_user, login_user
from werkzeug.security import generate_password_hash, check_password_hash
from server.models.User import Role, User, Permissions, UserRole, ResetToken, Role
from server.models.Properties import Property, Price
from server.models.Report import Report
from server.util.instances import db
from server.models.CloudinaryFileField import CLoudinaryFileUploadField




def initializeLogin(app):
    login_manager = LoginManager()
    login_manager.init_app(app)

    # Create user loader function
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

def initializeAdmin(admin):
    admin.add_view(UserAdminView(User, db.session, name="Users", url="users",menu_icon_value="fa-users",menu_icon_type="fas"))
    #admin.add_view(RoleAdminView(Role, db.session, category="Users", name="Roles", url="roles"))
    #admin.add_view(MyModelView(ResetToken, db.session, category="Users", name="Reset-tokens", url="reset-tokens"))
    admin.add_view(PropertyAdmin(Property, db.session, name="Properties",menu_icon_value="fa-building",menu_icon_type="fas"))
    admin.add_view(ReportView(Report, db.session, name='Reports',menu_icon_value="fa-file-pdf",menu_icon_type="fas"))


class MyModelView(ModelView):
    def is_accessible(self):
        if current_user and current_user.is_authenticated:
            userRole = UserRole.query.filter_by(user_id=current_user.id).first().json()
            return current_user.is_authenticated and userRole.get('role') == 'admin'

        else:
            False

    def is_visible(self):
        return True

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('admin.login_view', next=request.url))

class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for('.login_view'))

        
        return super(MyAdminIndexView, self).index()

    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        next = request.args.get('next')
        if current_user.is_authenticated:
            return redirect(url_for('.index'))

        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')

            if not email:
                flash('Email not provided')
                return render_template('admin/login.html')
            if not password:
                flash('Password not provided')
                return render_template('admin/login.html')

            user = User.query.filter_by(email=email.lower()).first()

            if user is None:
                flash('User with this email does not exist')
                return render_template('admin/login.html')

            if user.checkPassword(password) is False:
                flash('Invalid password')
                return render_template('admin/login.html')
            
            login_user(user)
            flash('Logged In successful')
            return redirect(next or url_for('.index'))

        return render_template('admin/login.html')

    @expose('/logout/', methods=('GET', 'POST'))
    def logout_view(self):
        logout_user()
        return redirect(url_for('.index'))


class RoleAdminView(MyModelView):
    form_choices = {'permissions': [(Permissions.READ, "Read"), (Permissions.WRITE, 'Write')]}

class UserAdminView(MyModelView):
    
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

class PropertyAdmin(MyModelView):
    form_choices = {'area': [('ikoyi', 'Ikoyi'), ('vi', 'Victoria Island'), ('lekki', 'Lekki'), ('oniru', 'Oniru')],
                    'state': [('lagos', 'Lagos')],
                    'bedrooms': [(1,'1 Bedroom'), (2, '2 Bedroom'), (3, '3 Bedroom'), (4, '4 Bedroom'), (5, '5 Bedroom'), (6, '6 Bedroom'), (7, '7 Bedroom')],
                    'type': [('Flat','Flat'), ('pent house', 'Pent House'), ('terrace', 'Terrace'), ("duplex", 'Duplex'), ("maisonette", 'Maisonette')]
                    }
    
    column_auto_select_related = True
    inline_models = [(Price,dict(form_columns=['id', 'year', 'amount']))]
    column_labels = {'built': 'Year built', 'serv_charge': 'Service charge'}
    column_sortable_list = ('area', 'bedrooms', 'name', 'built',)
    column_searchable_list = ('name', 'area', 'address', 'type')
    column_exclude_list=('created_at', 'updated_at')
    column_default_sort = ('name',False)
    can_export = True
    column_editable_list = ('name', 'bedrooms', 'address', 'area', 'serv_charge', 'type', 'sale_price')
    form_widget_args = {
        'facilities': {
            'rows': 6
        }
    }

class ReportView(MyModelView):

    form_overrides = dict(file= CLoudinaryFileUploadField)
    form_args = dict(file=dict( 
        base_path='https://res.cloudinary.com/kblinsurance/raw/upload/v1608312210/',
        ))