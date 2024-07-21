from flask_restful import Api
from flask import current_app, request, abort
import os

current_app.logger.info("Loading API...")
api = Api(current_app)

current_app.logger.info("The API is accessible from the following IP addresses: " + os.environ.get("FRONTEND_IP") + ", " + os.environ.get("BACKEND_IP"))


@current_app.before_request
def limit_remote_addr():
    if request.remote_addr != os.environ.get("FRONTEND_IP") and request.remote_addr != os.environ.get("BACKEND_IP"):
        abort(403)  # Forbidden

from src.api.auth import UserLogin, UserRegistration, VerifyAction, ExistsVerificationRequest
api.add_resource(UserLogin, "/user/login")
api.add_resource(UserRegistration, "/user/register")
api.add_resource(VerifyAction, "/user/verify")
api.add_resource(ExistsVerificationRequest, "/user/verify/exists")


current_app.logger.info("API loaded successfully")