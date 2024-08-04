from flask import jsonify, Response, current_app
from flask_restful import Resource, reqparse

class BaseResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()

    def handle_exception(self, e, *args, **kwargs):
        if isinstance(e, KeyError):
            current_app.logger.error(
                f"{self.__class__.__name__}: ({args}) -> Missing key in JSON payload: {e}",
                exc_info=True,
            )
            return {"error": f"Missing key in JSON payload: {e}"}, 400
        current_app.logger.error(
            f"{self.__class__.__name__}: ({args}) -> {e}", exc_info=True
        )
        return {"error": "Internal Server Error"}, 500
    
    def error_response(self, status_code, message, **kwargs) -> Response:
        response_dict = {
            "status": "error",
            "message": message,
            "errors": []
        }

        for field, error_message in kwargs.items():
            error_dict = {
                "field": field,
                "message": error_message
            }
            response_dict["errors"].append(error_dict)

        response = jsonify(response_dict)
        response.status_code = status_code
        return response
    
    def success_response(self, status_code, message, **kwargs) -> Response:
        response_dict = {
            "status": "success",
            "message": message,
            "content": [kwargs]
        }

        response = jsonify(response_dict)
        response.status_code = status_code
        return response