from flask import Flask
from config import Config
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager


def create_app(config_class=Config):
    app = Flask(__name__)

    try:
        app.config.from_object(config_class)
    except Exception as e:
        app.logger.error(f"Error while loading the configuration: {e}")


    from core.extensions import db
    try:
        db.init_app(app)
        migrate = Migrate(app, db)
    except Exception as e:
        app.logger.error(f"Error while initializing the database: {e}")

    try:
        jwt = JWTManager(app)
    except Exception as e:
        app.logger.error(f"Error while initializing the JWT manager: {e}")

    app.logger.info("App created successfully. Entering app context...")

    with app.app_context():
        try:
            import core.models
        except Exception as e:
            app.logger.error(f"Error while importing the models: {e}")

        try:
            import core.api
        except Exception as e:
            app.logger.error(f"Error while importing the API routes: {e}")

        try:
            db.create_all()
        except Exception as e:
            app.logger.error(f"Error while creating the database tables: {e}")

        # from core.services.rejector import Rejector
        # try:
        #     rejector = Rejector(app)
        #     rejector.start()
        # except Exception as e:
        #     app.logger.error(f"Error while initializing the rejector service: {e}")

        from apscheduler.schedulers.background import BackgroundScheduler
        from core.models.rejections import remove_expired_requests
        import atexit

        expired_rejections_scheduler = BackgroundScheduler()
        expired_rejections_scheduler.add_job(func=lambda: remove_expired_requests(app), trigger="interval", seconds=3)
        expired_rejections_scheduler.start()

        atexit.register(lambda: expired_rejections_scheduler.shutdown())

    return app
