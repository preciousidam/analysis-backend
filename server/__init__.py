import os
from flask import Flask, render_template, redirect, url_for
from flask_cors import CORS


###########ROUTES##################
from server.routes.auth import authRoute
from server.routes.properties import propertyRoute
from server.routes.statistics import statRoute
from server.routes.search import searchRoute
from server.routes.support import supportRoute

##############UTILITIES############
from server.util.instances import initializeDB, initializeJWT, initializeMail
from server.admin import initializeAdmin
from server.util.jsonEncoder import CustomJSONEncoder
    

#create_app(test_config=None):
def create_app(env):
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


    #initialize Database
    initializeDB(app)

    #initialize Mail
    initializeMail(app)

    #initialize JWT 
    initializeJWT(app)

    #initialize Admin 
    initializeAdmin(app)

    #initialize Cloudinary
    #initializeCloud(app)
   
    '''change jsonify default JSON encoder to a custom Encode
    ### to support Model encoding for {user, properties, etc}
    '''
    app.json_encoder = CustomJSONEncoder


    #Register Blueprints
    app.register_blueprint(authRoute)
    app.register_blueprint(propertyRoute)
    app.register_blueprint(statRoute)
    app.register_blueprint(searchRoute)
    app.register_blueprint(supportRoute)

    @app.route('/')
    def index():
        return redirect(url_for('admin.index'))

    #initialize CORS
    CORS(app)
    return app