from flask import current_app
from flask_restful import Resource, reqparse, fields, marshal_with
import logging
from src.extensions import verificator
import src.models.users as users
from src.api.base import BaseResource
import src.errors as errors

# Configure logging
logger = logging.getLogger(__name__)

user_registration_fields = {
    "message": fields.String,
}

verify_action_fields = {
    "id": fields.Integer,
    "email": fields.String,
    "password_hash": fields.String,
    "username": fields.String,
}

user_login_fields = {
    "id": fields.Integer,
    "email": fields.String,
    "password_hash": fields.String,
    "username": fields.String,
}


exists_verification_fields = {"exists": fields.Boolean}


class ExistsVerificationRequest(BaseResource):
    def __init__(self):
        super().__init__()
        self.parser.add_argument(
            "email", type=str, required=True, help="Email is required"
        )
        self.parser.add_argument(
            "type", type=int, required=True, help="Type is required"
        )

    @marshal_with(exists_verification_fields)
    def post(self):
        args = self.parser.parse_args()
        try:
            user_email, type = args["email"], args["type"]

            return {"exists": verificator.contains_request(user_email, type)}, 200
        except errors.VerificationError:
            return {"exists": True}, 200
        except Exception as e:
            return self.handle_exception(e), 500


class VerifyAction(BaseResource):
    def __init__(self):
        super().__init__()
        self.parser.add_argument(
            "email", type=str, required=True, help="Email is required"
        )
        self.parser.add_argument(
            "code", type=str, required=True, help="Code is required"
        )
        self.parser.add_argument(
            "type", type=int, required=True, help="Type is required"
        )

    @marshal_with(verify_action_fields)
    def post(self):
        """
        Handle POST requests for action verification.

        Expects:
        - email: User's email address
        - code: Verification code
        - type: Action type to be verified

        Returns:
        - JSON response with verification result and appropriate status code
        """
        args = self.parser.parse_args()
        try:
            user_email, code, type = args["email"], args["code"], args["type"]
            if not all(map(str.strip, [user_email, code])) or not type:
                return {"error": "Missing email or code", "data": False}, 400
            users.verify_action(verificator, type, user_email, code)

            user = users.get_user_by_email(user_email)

            return {
                "id": user.id,
                "email": user.email,
                "password_hash": user.password_hash,
                "username": user.username,
            }, 200
        except Exception as e:
            return self.handle_exception(e)


class UserLogin(BaseResource):
    def __init__(self):
        super().__init__()
        self.parser.add_argument(
            "email", type=str, required=True, help="Email is required"
        )
        self.parser.add_argument(
            "password", type=str, required=True, help="Password is required"
        )

    @marshal_with(user_login_fields)
    def post(self):
        args = self.parser.parse_args()
        try:
            user_email, user_password = args["email"], args["password"]

            user = users.get_user_by_email(user_email)

            if not user or not users.check_user_password(user.id, user_password):
                return {"error": "Invalid email or password"}, 401

            return {
                "id": user.id,
                "email": user.email,
                "password_hash": user.password_hash,
                "username": user.username,
            }, 200, 200
        except Exception as e:
            return self.handle_exception(e)


class UserRegistration(BaseResource):
    def __init__(self):
        super().__init__()
        self.parser.add_argument(
            "username", type=str, required=True, help="Username is required"
        )
        self.parser.add_argument(
            "email", type=str, required=True, help="Email is required"
        )
        self.parser.add_argument(
            "password", type=str, required=True, help="Password is required"
        )

    @marshal_with(user_registration_fields)
    def post(self):
        args = self.parser.parse_args()
        try:
            users.register_user(verificator, **args)
            return {"message": "Registration request sent"}, 200
        except Exception as e:
            return self.handle_exception(e)
