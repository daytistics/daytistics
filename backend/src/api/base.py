from flask import current_app
from flask_restful import Api, Resource, reqparse

class BaseResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()

    def handle_exception(self, e):
        if isinstance(e, KeyError):
            current_app.logger.error(f"Missing key in JSON payload: {e}")
            return {"error": f"Missing key in JSON payload: {e}"}, 400
        current_app.logger.error(f"Unexpected error: {e}", exc_info=True)
        return {"error": "Internal Server Error"}, 500