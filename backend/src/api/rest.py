from flask_restful import Api
from flask import current_app, request, abort
import os
import src.api.routes as routes

current_app.logger.info("Loading API...")
api = Api(current_app)

current_app.logger.info("The API is accessible from the following IP addresses: {}, {}".format(
    current_app.config.get("FRONTEND_IP"),
    current_app.config.get("BACKEND_IP")
))

@current_app.before_request
def limit_remote_addr():
    if request.remote_addr != os.environ.get("FRONTEND_IP") and request.remote_addr != os.environ.get("BACKEND_IP"):
        abort(403)  # Forbidden

import src.api.auth as auth

api.add_resource(auth.ExistsRegistrationRequest, routes.EXISTS_REGISTRATION_REQUEST_ROUTE)
api.add_resource(auth.ExistsChangePasswordRequest, routes.EXISTS_CHANGE_PASSWORD_REQUEST_ROUTE)
api.add_resource(auth.ExistsResetPasswordRequest, routes.EXISTS_RESET_PASSWORD_REQUEST_ROUTE)
api.add_resource(auth.ExistsDeleteAccountRequest, routes.EXISTS_DELETE_ACCOUNT_REQUEST_ROUTE)

api.add_resource(auth.VerifyRegistrationRequest, routes.VERIFY_REGISTRATION_REQUEST_ROUTE)
api.add_resource(auth.VerifyChangePasswordRequest, routes.VERIFY_CHANGE_PASSWORD_REQUEST_ROUTE)
api.add_resource(auth.VerifyResetPasswordRequest, routes.VERIFY_RESET_PASSWORD_REQUEST_ROUTE)
api.add_resource(auth.VerifyDeleteAccountRequest, routes.VERIFY_DELETE_ACCOUNT_REQUEST_ROUTE)

api.add_resource(auth.UserRegistration, routes.USER_REGISTRATION_ROUTE)

current_app.logger.info("API loaded successfully")