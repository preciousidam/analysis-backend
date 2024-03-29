import os
from flask import Flask, render_template, redirect, url_for, jsonify
from flask_cors import CORS
from flask_admin import Admin


###########ROUTES##################
from server.routes.auth import authRoute
from server.routes.properties import propertyRoute
from server.routes.statistics import statRoute
from server.routes.search import searchRoute
from server.routes.support import supportRoute
from server.routes.reports import reportRoute
from server.models.User import User, UserRole

##############UTILITIES############
from server.util.instances import initializeDB, initializeJWT, initializeMail, initializeMigrate
from server.admin import initializeAdmin, MyAdminIndexView, initializeLogin
from server.util.jsonEncoder import CustomJSONEncoder


# create_app(test_config=None):
def create_app(env='development'):
    # create and configure the app

    app = Flask(__name__, instance_relative_config=True)

    if env == 'development':
        # load the instance dev config, if it exists, when not testing
        app.config.from_object('instance.config.DevelopementConfig')

    elif env == 'production':
        # load the instance production config, if it exists, when not testing
        app.config.from_object('instance.config.ProductionConfig')

    elif env == 'testing':
        # load the test config if passed in
        app.config.from_object('instance.config.TestConfig')

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    admin = Admin(app, 'Napims Admin',
                  index_view=MyAdminIndexView(name="Home", url='/', menu_icon_value="fa-home", menu_icon_type="fas", template="admin/index.html"), template_mode="bootstrap4")

    # initialize Database
    initializeDB(app)

    # initialize Mail
    initializeMail(app)

    # initialize JWT
    initializeJWT(app)

    # initialize Admin
    initializeAdmin(admin)

    # initialize Flask_login
    initializeLogin(app)

    # initialize Flask_Migrate
    initializeMigrate(app)

    '''change jsonify default JSON encoder to a custom Encode
    ### to support Model encoding for {user, properties, etc}
    '''
    app.json_encoder = CustomJSONEncoder

    # Register Blueprints
    app.register_blueprint(authRoute)
    app.register_blueprint(propertyRoute)
    app.register_blueprint(statRoute)
    app.register_blueprint(searchRoute)
    app.register_blueprint(supportRoute)
    app.register_blueprint(reportRoute)

    @app.after_request
    def add_header(r):
        """
        Add headers to both force latest IE rendering engine or Chrome Frame,
        and also to cache the rendered page for 10 minutes.
        """
        r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        r.headers["Pragma"] = "no-cache"
        r.headers["Expires"] = "0"
        r.headers['Cache-Control'] = 'public, max-age=0'
        return r

    @app.route('/test')
    def index():

        return render_template('admin/base.html')

    # initialize CORS
    CORS(app)
    return app
