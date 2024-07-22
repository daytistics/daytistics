from flask import Flask
from src.extensions import db
from config import Config
from flask_migrate import Migrate
from dotenv import load_dotenv

load_dotenv()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate = Migrate(app, db)

    with app.app_context():
        import src.models  
        import src.api

        try:
            db.create_all()  
        except Exception as e:
            app.logger.error(f"Error while creating the database:")# {str(e)}")

    return app
