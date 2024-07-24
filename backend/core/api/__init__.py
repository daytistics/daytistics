from flask_restful import Api, Resource, reqparse
from flask import current_app, request, abort
import os
import core.utils.routes as routes

class BaseResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()

    def handle_exception(self, e, *args, **kwargs):
        if isinstance(e, KeyError):
            current_app.logger.error(f"{self.__class__.__name__}: ({args}) -> Missing key in JSON payload: {e}", exc_info=True)
            return {"error": f"Missing key in JSON payload: {e}"}, 400
        current_app.logger.error(f"{self.__class__.__name__}: ({args}) -> {e}", exc_info=True)
        return {"error": "Internal Server Error"}, 500


api = Api(current_app)

current_app.logger.info("The API is accessible from the following IP addresses: {} (Frontend), {} (Backend)".format(
    current_app.config.get("FRONTEND_IP"),
    current_app.config.get("BACKEND_IP")
))

@current_app.before_request
def limit_remote_addr():
    with current_app.app_context():
        if request.remote_addr != current_app.config.get("FRONTEND_IP") and request.remote_addr != current_app.config.get("BACKEND_IP"):
            abort(403)


from core.api import users

api.add_resource(users.ExistsRegistrationRequest, routes.EXISTS_REGISTRATION_REQUEST_ROUTE)
api.add_resource(users.ExistsChangePasswordRequest, routes.EXISTS_CHANGE_PASSWORD_REQUEST_ROUTE)
api.add_resource(users.ExistsResetPasswordRequest, routes.EXISTS_RESET_PASSWORD_REQUEST_ROUTE)
api.add_resource(users.ExistsDeleteAccountRequest, routes.EXISTS_DELETE_ACCOUNT_REQUEST_ROUTE)

api.add_resource(users.VerifyRegistrationRequest, routes.VERIFY_REGISTRATION_REQUEST_ROUTE)
api.add_resource(users.VerifyChangePasswordRequest, routes.VERIFY_CHANGE_PASSWORD_REQUEST_ROUTE)
api.add_resource(users.VerifyResetPasswordRequest, routes.VERIFY_RESET_PASSWORD_REQUEST_ROUTE)
api.add_resource(users.VerifyDeleteAccountRequest, routes.VERIFY_DELETE_ACCOUNT_REQUEST_ROUTE)

api.add_resource(users.UserChangeUsername, routes.CHANGE_USERNAME_ROUTE)
api.add_resource(users.UserRegistration, routes.USER_REGISTRATION_ROUTE)
api.add_resource(users.UserLogin, routes.USER_LOGIN_ROUTE)
api.add_resource(users.UserChangePassword, routes.CHANGE_USER_PASSWORD_ROUTE)

api.add_resource(users.UserCheckPassword, routes.CHECK_PASSWORD_ROUTE)
api.add_resource(users.UserInformation, routes.USER_INFORMATION_ROUTE)

api.add_resource(users.TokenRefresh, routes.TOKEN_REFRESH_ROUTE)
api.add_resource(users.TokenEmail, routes.TOKEN_EMAIL_ROUTE)
