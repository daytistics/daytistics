from flask_restful import Api
from flask import current_app, request, abort
import os

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

api.add_resource(auth.ExistsRegistrationRequest, "/user/verify/registration/exists")
api.add_resource(auth.ExistsChangePasswordRequest, "/user/verify/change_password/exists")
api.add_resource(auth.ExistsResetPasswordRequest, "/user/verify/reset_password/exists")
api.add_resource(auth.ExistsDeleteAccountRequest, "/user/verify/delete_account/exists")

api.add_resource(auth.VerifyRegistrationRequest, "/user/verify/registration")
api.add_resource(auth.VerifyChangePasswordRequest, "/user/verify/change_password")
api.add_resource(auth.VerifyResetPasswordRequest, "/user/verify/reset_password")
api.add_resource(auth.VerifyDeleteAccountRequest, "/user/verify/delete_account")

current_app.logger.info("API loaded successfully")