from flask import Flask
from core.extensions import db
from config import Config
from flask_migrate import Migrate
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
import os

def create_app(config_class=Config):
    app = Flask(__name__)

    app.config.from_object(config_class)
    
    db.init_app(app)
    migrate = Migrate(app, db)

    jwt = JWTManager(app)

    with app.app_context():
        import core.models  
        import core.api

        try:
            db.create_all()  
        except Exception as e:
            app.logger.error(f"Error while creating the database:")

    return app
