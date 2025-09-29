from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager 
from flask_jwt_extended import JWTManager 
from flask_marshmallow import Marshmallow 
from flask_cors import CORS 

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager() 
login.login_view = 'main.login' 
jwt = JWTManager() 
ma = Marshmallow() 

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Enable CORS
    CORS(app)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app) 
    jwt.init_app(app) 
    ma.init_app(app) 

    from app.main import bp as main_bp
    
    app.register_blueprint(main_bp, url_prefix='/api/v1')

    return app

from app import models