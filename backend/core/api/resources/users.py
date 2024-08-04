from flask import current_app
from core.extensions import verificator
from core.models import users
from core.utils.emails import is_valid_email
from core.utils.users import is_valid_username, is_good_password
from core.utils.verification import is_valid_verification_code
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    create_refresh_token,
    jwt_required,
    decode_token,
)
from core import errors
from core.models import rejections
from core.api.resources import BaseResource



class ExistsRegistrationRequest(BaseResource):
    def __init__(self):
        super().__init__()
        self.parser.add_argument(
            "email", type=str, required=True, help="Email is required"
        )

    def post(self):
        args = self.parser.parse_args()
        try:
            email = args["email"]

            if email is None or not email.strip():
                return self.error_response(400, "Missing or invalid input data", email="Missing email")

            if not is_valid_email(email):
                return self.error_response(400, "Invalid email", email="Email does not satisfy the requirements (between 3 and 20 characters, valid domain name, contains @)")

            if not users.is_user_existing_by_email(email):
                return self.error_response(404, "User not found", email="User not found by email")

            return self.success_response(200, "User has a registration request", has_request=verificator.exists_registration_request(email))

        except Exception as e:
            self.handle_exception(e, args)


class VerifyRegistrationRequest(BaseResource):
    def __init__(self):
        super().__init__()
        self.parser.add_argument(
            "email", type=str, required=True, help="Email is required"
        )
        self.parser.add_argument(
            "code", type=str, required=True, help="Code is required"
        )

    def post(self):
        args = self.parser.parse_args()
        current_app.logger.info(verificator.registration_requests)
        try:
            email, code = args["email"], args["code"]

            if email == None or not email.strip():
                return self.error_response(400, "Missing or invalid input data", email="Missing email")

            if code == None or not code.strip():
                return self.error_response(400, "Missing or invalid input data", code="Missing code")

            if not is_valid_email(email):
                return self.error_response(400, "Invalid email", email="Email does not satisfy the requirements (between 3 and 20 characters, valid domain name, contains @)")

            if not is_valid_verification_code(code):
                return self.error_response(400, "Invalid code", code="Code does not satisfy the requirements (6 characters, alphanumeric)")

            if not verificator.exists_registration_request(email):
                return self.error_response(404, "No registration request found for this email", email="No registration request found for this email")


            # TODO: DOCUMENTATION!!!!!
            # ! I know this is a bad practice, but I'm not sure how to handle this properly
            try:
                verificator.verify_registration_request(email, code)
            except errors.VerificationTemporarilyRejectedError:
                return self.error_response(601, "Verification temporarily rejected", verification_rejections="> 3")
            except errors.VerificationFailureLimitExceededError:
                return self.error_response(602, "Verification failure limit exceeded", failures="> 3")
            except errors.InvalidVerificationCodeError:
                return self.error_response(603, "Invalid code", code="Not in verification requests")

            return self.success_response(200, "Verified registration request")

        except Exception as e:
            self.handle_exception(e, args)


class RegisterUser(BaseResource):
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

    def post(self):
        args = self.parser.parse_args()

        try:
            if args["email"] == None or not args["email"].strip():
                return self.error_response(400, "Missing or invalid input data", email="Missing email")

            if args["username"] == None or not args["username"].strip():
                return self.error_response(400, "Missing or invalid input data", username="Missing username")

            if args["password"] == None or not args["password"].strip():
                return self.error_response(400, "Missing or invalid input data", password="Missing password")

            if not is_valid_email(args["email"]):
                return self.error_response(400, "Invalid email", email="Email does not satisfy the requirements (between 3 and 20 characters, valid domain name, contains @)")

            if users.is_user_existing_by_email(args["email"]):
                return self.error_response(409, "User already exists", email="User already exists")

            if not is_valid_username(args["username"]):
                return self.error_response(400, "Invalid username", username="Username does not satisfy the requirements (between 3 and 20 characters, alphanumeric)")

            if not is_good_password(args["password"]):
                return self.error_response(400, "Invalid password", password="Password does not satisfy the requirements (between 8 and 20 characters, at least one uppercase letter, one lowercase letter, one digit, one special character)")

            users.register_user(args["username"], args["password"], args["email"])

            return self.success_response(201, "User registered")
        except Exception as e:
            self.handle_exception(e, args)


class LoginUser(BaseResource):
    def __init__(self):
        super().__init__()
        self.parser.add_argument(
            "email", type=str, required=True, help="Email is required"
        )
        self.parser.add_argument(
            "password", type=str, required=True, help="Password is required"
        )

    def post(self):
        args = self.parser.parse_args()
        email, password = args["email"], args["password"]

        try:
            if email is None or not email.strip():
                return self.error_response(400, "Missing or invalid input data", email="Missing email")

            if password is None or not password.strip():
                return self.error_response(400, "Missing or invalid input data", password="Missing password")

            if not is_valid_email(email):
                return self.error_response(400, "Invalid email", email="Email does not satisfy the requirements (between 3 and 20 characters, valid domain name, contains @)")

            if not users.is_user_existing_by_email(email):
                return self.error_response(404, "User not found", email="User not found by email")

            if not users.check_user_password(email, password):
                return self.error_response(401, "Invalid password", password="Password is incorrect")

            access_token = create_access_token(identity=email)
            refresh_token = create_refresh_token(identity=email)

            return self.success_response(200, "User logged in", access_token=access_token, refresh_token=refresh_token)
        except Exception as e:
            self.handle_exception(e, args)


class RefreshUserToken(BaseResource):
    def __init__(self):
        super().__init__()

    @jwt_required(refresh=True)
    def post(self):
        from jwt import exceptions

        try:
            email = get_jwt_identity()
            access_token = create_access_token(identity=email)
            return self.success_response(200, "Token refreshed", access_token=access_token)

        except exceptions.ExpiredSignatureError:
            return self.error_response(401, "Token has expired", token="Token has expired")
        except exceptions.InvalidTokenError:
            return self.error_response(401, "Invalid token", token="Token is invalid")
        except Exception as e:
            self.handle_exception(e)


class GetUserEmail(BaseResource):
    def __init__(self):
        super().__init__()

    @jwt_required()
    def get(self):
        try:
            email = get_jwt_identity()

            return self.success_response(200, "Email retrieved", email=email)
        except Exception as e:
            self.handle_exception(e)


class UserCheckPassword(BaseResource):
    def __init__(self):
        super().__init__()
        self.parser.add_argument(
            "email", type=str, required=True, help="Email is required"
        )
        self.parser.add_argument(
            "password", type=str, required=True, help="Password is required"
        )

    def post(self):
        args = self.parser.parse_args()
        email, password = args["email"], args["password"]

        try:
            if email == None or not email.strip():
                return self.error_response(400, "Missing or invalid input data", email="Missing email")

            if password == None or not password.strip():
                return self.error_response(400, "Missing or invalid input data", password="Missing password")

            if not is_valid_email(email):
                return self.error_response(400, "Invalid email", email="Email does not satisfy the requirements (between 3 and 20 characters, valid domain name, contains @)")

            if not users.is_user_existing_by_email(email):
                return self.error_response(404, "User not found", email="User not found by email")

            if not users.check_user_password(email, password):
                return self.error_response(401, "Invalid password", password="Password is incorrect")

            return self.success_response(200, "Password is correct")
        except Exception as e:
            self.handle_exception(e, args)


class GetUserInformation(BaseResource):
    def __init__(self):
        super().__init__()

    @jwt_required()
    def get(self):
        try:
            email = get_jwt_identity()
            user = users.get_user_by_email(email)

            return self.success_response(200, "User information retrieved", id=user.id, username=user.username, email=user.email, created_at=user.created_at, role=user.role, verification=user.verification, verification_rejections=user.verification_rejections)
        except Exception as e:
            self.handle_exception(e)


class ExistsUser(BaseResource):
    def __init__(self):
        super().__init__()
        self.parser.add_argument(
            "email", type=str, required=True, help="Email is required"
        )

    def post(self):
        args = self.parser.parse_args()
        email = args["email"]

        try:
            if email == None or not email.strip():
                return self.error_response(400, "Missing or invalid email", email="Missing email")

            if not is_valid_email(email):
                return self.error_response(400, "Invalid email", email="Email does not satisfy the requirements (between 3 and 20 characters, valid domain name, contains @)")

            return self.success_response(200, "User exists", exists=users.is_user_existing_by_email(email))
        except Exception as e:
            self.handle_exception(e, args)


class ResendRegistrationEmail(BaseResource):
    def __init__(self):
        super().__init__()
        self.parser.add_argument(
            "email", type=str, required=True, help="Email is required"
        )

    def post(self):
        args = self.parser.parse_args()
        email = args["email"]

        current_app.logger.info(verificator.registration_requests)

        try:
            if email == None or not email.strip():
                return {"error": "Missing or invalid email"}, 400

            if not is_valid_email(email):
                return self.error_response(400, "Invalid email", email="Email does not satisfy the requirements (between 3 and 20 characters, valid domain name, contains @)")

            if not users.is_user_existing_by_email(email):
                return self.error_response(404, "User not found", email="User not found by email")

            verificator.resend_registration_request(email)
            return self.success_response(200, "Registration request resent")
        except Exception as e:
            self.handle_exception(e, args)

class HasAuthRejection(BaseResource):

    @jwt_required()
    def get(self):
        email = get_jwt_identity()

        try:
            if email == None or not email.strip():
                return self.error_response(400, "Missing or invalid input data", email="Missing email")

            if not is_valid_email(email):
                return self.error_response(400, "Invalid email", email="Email does not satisfy the requirements (between 3 and 20 characters, valid domain name, contains @)")

            return self.success_response(200, "User has a rejection", has_rejection=rejections.has_auth_rejection(email))
        except Exception as e:
            self.handle_exception(e, email)

class HasExceededFailureLimit(BaseResource):

    @jwt_required()
    def get(self):
        email = get_jwt_identity()

        try:
            if email == None or not email.strip():
                return self.error_response(400, "Missing or invalid input data", email="Missing email")

            if not is_valid_email(email):
                return self.error_response(400, "Invalid email", email="Email does not satisfy the requirements (between 3 and 20 characters, valid domain name, contains @)")
            
            if not verificator.exists_registration_request(email):
                return self.error_response(404, "No registration request found for this email", email="No registration request found for this email")

            return self.success_response(200, "User has exceeded failure limit", limit_exceeded=verificator.has_exceeded_failure_limit(email))
        except Exception as e:
            self.handle_exception(e, email)