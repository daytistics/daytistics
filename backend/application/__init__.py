from flask import Flask
from application.extensions import db
from config import Config
from flask_migrate import Migrate
from application.commands import load_commands

from dotenv import load_dotenv

load_dotenv()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    with app.app_context():
        db.init_app(app)
        migrate = Migrate(app, db)

        try:
            db.create_all()
        except Exception as e:
            print(e)

        from application.main import bp as main_bp
        app.register_blueprint(main_bp)

        load_commands(app)

        return app
