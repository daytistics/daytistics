from flask import current_app
from src.services.verify import is_valid_verification_code
from src.extensions import verificator
import src.models.users as users
from src.api.base import BaseResource
from src.utils.emails import is_valid_email
from src.utils.users import is_valid_username, is_good_password
from flask_jwt_extended import create_access_token, decode_token, get_jwt_identity, create_refresh_token, jwt_required

class ExistsRegistrationRequest(BaseResource):
    def __init__(self):
        super().__init__()
        self.parser.add_argument("email", type=str, required=True, help="Email is required")

    def post(self):
        args = self.parser.parse_args()
        try:
            email = args["email"]

            if email is None or not email.strip():
                return {"error": "Missing or invalid email"}, 400

            if not is_valid_email(email):
                return {"error": "Invalid email"}, 400

            return {"exists": verificator.exists_registration_request(email)}, 200
        except Exception as e:
            current_app.logger.exception(f"Unhandled exception in ExistsRegistrationRequest (POST: {args})")
            return {"error": str(e)}, 500

class ExistsChangePasswordRequest(BaseResource):
    def __init__(self):
        super().__init__()
        self.parser.add_argument("email", type=str, required=True, help="Email is required")

    def post(self):
        args = self.parser.parse_args()
        try:
            email = args["email"]

            if email is None or not email.strip():
                return {"error": "Missing or invalid email"}, 400
            
            if not is_valid_email(email):
                return {"error": "Invalid email"}, 400

            return {"exists": verificator.exists_change_password_request(email)}, 200
        except Exception as e:
            current_app.logger.exception(f"Unhandled exception in ExistsChangePasswordRequest (POST: {args})")
            return {"error": str(e)}, 500

class ExistsResetPasswordRequest(BaseResource):
    def __init__(self):
        super().__init__()
        self.parser.add_argument("email", type=str, required=True, help="Email is required")

    def post(self):
        args = self.parser.parse_args()
        try:
            email = args["email"]

            if email is None or not email.strip():
                return {"error": "Missing or invalid email"}, 400
            
            if not is_valid_email(email):
                return {"error": "Invalid email"}, 400

            return {"exists": verificator.exists_reset_password_request(email)}, 200
        except Exception as e:
            current_app.logger.exception(f"Unhandled exception in ExistsResetPasswordRequest (POST: {args})")
            return {"error": str(e)}, 500
        
class ExistsDeleteAccountRequest(BaseResource):
    def __init__(self):
        super().__init__()
        self.parser.add_argument("email", type=str, required=True, help="Email is required")

    def post(self):
        args = self.parser.parse_args()
        try:
            email = args["email"]

            if email is None or not email.strip():
                return {"error": "Missing or invalid email"}, 400
            
            if not is_valid_email(email):
                return {"error": "Invalid email"}, 400

            return {"exists": verificator.exists_delete_account_request(email)}, 200
        except Exception as e:
            current_app.logger.exception(f"Unhandled exception in ExistsDeleteAccountRequest (POST: {args})")
            return {"error": str(e)}, 500

class VerifyRegistrationRequest(BaseResource):
    def __init__(self):
        super().__init__()
        self.parser.add_argument("email", type=str, required=True, help="Email is required")
        self.parser.add_argument("code", type=str, required=True, help="Code is required")

    def post(self):
        args = self.parser.parse_args()
        try:
            email, code = args["email"], args["code"]

            from flask_jwt_extended import get_jwt_identity

            if email == None or code == None or not email.strip() or not code.strip():
                return {"error": "Invalid input data"}, 400

            if not is_valid_email(email):
                return {"error": "Invalid email"}, 400
            
            if not is_valid_verification_code(code):
                return {"error": "Invalid code format"}, 400

            if not verificator.exists_registration_request(email):
                return {"error": "No registration request found for this email"}, 404
            
            if not verificator.registration_requests[email]["code"] == code:
                return {"error": "Invalid code"}, 400

            verificator.verify_registration_request(email, code)

            return {"message": "Verified registration request"}, 200

        except Exception as e:
            current_app.logger.exception(f"Unhandled exception in VerifyRegistrationRequest (POST: {args})")
            return {"error": str(e)}, 500

class VerifyChangePasswordRequest(BaseResource):
    def __init__(self):
        super().__init__()
        self.parser.add_argument("email", type=str, required=True, help="Email is required")
        self.parser.add_argument("code", type=str, required=True, help="Code is required")

    def post(self):
        args = self.parser.parse_args()
        try:
            email, code = args["email"], args["code"]

            if email == None or code == None or not email.strip() or not code.strip():
                return {"error": "Invalid input data"}, 400
            
            if not is_valid_email(email):
                return {"error": "Invalid email"}, 400
            
            if not is_valid_verification_code(code):
                return {"error": "Invalid code format"}, 400

            if not verificator.exists_change_password_request(email):
                return {"error": "No change password request found for this email"}, 404
            
            if not verificator.change_password_requests[email]["code"] == code:
                return {"error": "Invalid code"}, 400

            verificator.verify_change_password_request(email, code)

            return {"message": "Verified change password request"}, 200

        except Exception as e:
            current_app.logger.exception(f"Unhandled exception in VerifyChangePasswordRequest (POST: {args})")
            return {"error": str(e)}, 500

class VerifyResetPasswordRequest(BaseResource):
    def __init__(self):
        super().__init__()
        self.parser.add_argument("email", type=str, required=True, help="Email is required")
        self.parser.add_argument("code", type=str, required=True, help="Code is required")

    def post(self):
        args = self.parser.parse_args()
        try:
            email, code = args["email"], args["code"]

            if not email.strip() or not code.strip():
                return {"error": "Invalid input data"}, 400
            
            if not is_valid_email(email):
                return {"error": "Invalid email"}, 400
            
            if not is_valid_verification_code(code):
                return {"error": "Invalid code format"}, 400

            if not verificator.exists_reset_password_request(email):
                return {"error": "No reset password request found for this email"}, 404
            
            if not verificator.reset_password_requests[email]["code"] == code:
                return {"error": "Invalid code"}, 400

            verificator.verify_reset_password_request(email, code)

            return {"message": "Verified reset password request"}, 200

        except Exception as e:
            current_app.logger.exception(f"Unhandled exception in VerifyResetPasswordRequest (POST: {args})")
            return {"error": str(e)}, 500
        
class VerifyDeleteAccountRequest(BaseResource):
    def __init__(self):
        super().__init__()
        self.parser.add_argument("email", type=str, required=True, help="Email is required")
        self.parser.add_argument("code", type=str, required=True, help="Code is required")

    def post(self):
        args = self.parser.parse_args()
        try:
            email, code = args["email"], args["code"]

            if email == None or code == None  or not email.strip() or not code.strip():
                return {"error": "Invalid input data"}, 400
            
            if not is_valid_email(email):
                return {"error": "Invalid email"}, 400
            
            if not is_valid_verification_code(code):
                return {"error": "Invalid code format"}, 400

            if not verificator.exists_delete_account_request(email):
                return {"error": "No delete account request found for this email"}, 404
            
            if not verificator.delete_account_requests[email]["code"] == code:
                return {"error": "Invalid code"}, 400

            verificator.verify_delete_account_request(email, code)

            return {"message": "Verified delete account request"}, 200

        except Exception as e:
            current_app.logger.exception(f"Unhandled exception in VerifyDeleteAccountRequest (POST: {args})")
            return {"error": str(e)}, 500

class UserRegistration(BaseResource):
    def __init__(self):
        super().__init__()
        self.parser.add_argument("username", type=str, required=True, help="Username is required")
        self.parser.add_argument("email", type=str, required=True, help="Email is required")
        self.parser.add_argument("password", type=str, required=True, help="Password is required")

    def post(self):
        args = self.parser.parse_args()

        try:

            if args["email"] == None or args["username"] == None or args["password"] == None or not args["username"].strip() or not args["email"].strip() or not args["password"].strip():
                return {"error": "Missing or invalid input data"}, 400
            
            if not is_valid_email(args["email"]):
                return {"error": "Invalid email"}, 400
            
            if verificator.exists_registration_request(args["email"]):
                return {"error": "Registration request already exists"}, 409
            
            if users.is_user_existing_by_email(args["email"]):
                
                return {"error": "Email already in use"}, 409
            
            if not is_valid_username(args["username"]):
                return {"error": "Invalid username"}, 400
            
            # if not is_string_content_allowed(args["username"]):
            #    return {"error": "Username contains explicit content"}
            

            if not is_good_password(args["password"]):
                return {"error": "Bad password"}, 400

            users.register_user(args["username"], args["password"], args["email"])
            return {"message": "Registration request sent"}, 200
        except Exception as e:
            current_app.logger.exception(f"Unhandled exception in UserRegistration (POST: {args})")

            return {"error": str(e)}, 500

class UserLogin(BaseResource):
    def __init__(self):
        super().__init__()
        self.parser.add_argument("email", type=str, required=True, help="Email is required")
        self.parser.add_argument("password", type=str, required=True, help="Password is required")

    def post(self):
        args = self.parser.parse_args()
        email, password = args["email"], args["password"]

        try:
            if email == None or password == None or not email.strip() or not password.strip():
                return {"error": "Missing or invalid input data"}, 400
            
            if not is_valid_email(email):
                return {"error": "Invalid email"}, 400
            
            if not users.is_user_existing_by_email(email):
                return {"error": "User not found"}, 404
            
            if not users.check_user_password(email, password):
                return {"error": "Invalid password"}, 401

            access_token = create_access_token(identity=email)
            refresh_token = create_refresh_token(identity=email)
            return {"access_token": access_token, "refresh_token": refresh_token}, 200
        except Exception as e:

            with open("error.log", "a") as f:
                f.write(str(e))

            current_app.logger.exception(f"Unhandled exception in UserLogin (POST: {args})")
            return {"error": str(e)}, 500

class TokenRefresh(BaseResource):

    def __init__(self):
        super().__init__()


    @jwt_required(refresh=True)
    def post(self):

        from jwt import exceptions
        try:
            email = get_jwt_identity()
            access_token = create_access_token(identity=email)
            return {"access_token": access_token}, 200
        
        except exceptions.ExpiredSignatureError:
            return {"error": "Token has expired"}, 401
        except exceptions.InvalidTokenError:
            return {"error": "Invalid token"}, 401
        except Exception as e:
            current_app.logger.exception(f"Unhandled exception in TokenRefresh")



            return {"error": str(e)}, 500

class TokenEmail(BaseResource):
    def __init__(self):
        super().__init__()

    @jwt_required() 
    def get(self):
        try:
            email = get_jwt_identity()

            return {"email": email}, 200
        except Exception as e:
            return {"error": str(e)}, 500

class UserChangeUsername(BaseResource):
    def __init__(self):
        super().__init__()
        self.parser.add_argument('email', type=str, required=True, help='Email is required')
        self.parser.add_argument('new_username', type=str, required=True, help='New username is required')

    def post(self):
        try:
            args = self.parser.parse_args()
            email, new_username = args['email'], args['new_username']

            current_app.logger.info(f"Changing username for {email} to {new_username}")
            current_app.logger.info(f"Args: {args}")

            if email == None or new_username == None or not email.strip() or not new_username.strip():
                current_app.logger.error(f"Missing or invalid input data: {args}")
                return {"error": "Missing or invalid input data"}, 400

            if not is_valid_email(email):
                current_app.logger.error(f"Invalid email: {email}")
                return {"error": "Invalid email"}, 400
            
            if not users.is_user_existing_by_email(email):
                current_app.logger.error(f"Email not in use: {email}")
                return {"error": "Email not in use"}, 400
            
            if not is_valid_username(new_username):
                current_app.logger.error(f"Invalid username: {new_username}")
                return {"error": "Invalid username"}, 400
            
            users.change_username(email, new_username)
            return {"message": "Username changed successfully"}, 200
        except Exception as e:
            return {"error": str(e)}, 500        
        
class UserChangePassword(BaseResource):
    def __init__(self):
        super().__init__()
        self.parser.add_argument("email", type=str, required=True, help="Email is required")
        self.parser.add_argument("new_password", type=str, required=True, help="New password is required")

    def post(self):
        args = self.parser.parse_args()
        email, new_password = args["email"], args["new_password"]

        try:

            if email == None or new_password == None or not email.strip() or not new_password.strip():
                return {"error": "Missing or invalid input data"}, 400
            
            if not is_valid_email(email):
                return {"error": "Invalid email"}, 400
            
            if not users.is_user_existing_by_email(email):
                current_app.logger.error(f"User not found: {args}")
                return {"error": "User not found"}, 404
            
            if verificator.exists_change_password_request(args["email"]):
                return {"error": "Change password request already exists"}, 409
            
            if not is_good_password(new_password):
                return {"error": "Bad password"}, 400

            users.change_user_password(email, new_password)
            return {"message": "Change password request sent"}, 200
        except Exception as e:
            current_app.logger.exception(f"Unhandled exception in UserChangePassword (POST: {args})")

            return {"error": str(e)}, 500