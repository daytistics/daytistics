import random, threading
from datetime import datetime, timedelta
import src.errors as errors
import time
from src.extensions import db


class Verificator:

    _instance = None

    def __init__(self):
        self.registration_requests = {}
        self.change_password_requests = {}
        self.reset_password_requests = {}
        self.delete_account_requests = {}
        self._stop_event = threading.Event()
        self._scheduler_thread = threading.Thread(target=self._remove_expired_requests_loop)
        self._scheduler_thread.daemon = True  # Keep this as True for now
        self._scheduler_thread.start()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def remove_expired_requests(self):

        current_time = datetime.now()
        five_minutes_ago = current_time - timedelta(minutes=5)
        
        for email, request in list(self.registration_requests.items()):
            if request["timestamp"] < five_minutes_ago:
                del self.registration_requests[email]

        for email, request in list(self.change_password_requests.items()):
            if request["timestamp"] < five_minutes_ago:
                del self.change_password_requests[email]

        for email, request in list(self.reset_password_requests.items()):
            if request["timestamp"] < five_minutes_ago:
                del self.reset_password_requests[email]

        for email, request in list(self.delete_account_requests.items()):
            if request["timestamp"] < five_minutes_ago:
                del self.delete_account_requests[email]

    def _remove_expired_requests_loop(self):
        while not self._stop_event.is_set():
            self.remove_expired_requests()
            if not self._stop_event.is_set():
                time.sleep(10)

    def stop_scheduler(self):

        self._stop_event.set()
        self._scheduler_thread.join()

    def exists_registration_request(self, email) -> bool:
        return email in self.registration_requests
    
    def exists_change_password_request(self, email) -> bool:
        return email in self.change_password_requests
    
    def exists_reset_password_request(self, email) -> bool:
        return email in self.reset_password_requests
    
    def exists_delete_account_request(self, email) -> bool:
        return email in self.delete_account_requests

    def add_registration_request(self, email, username, password_hash, role) -> str:
            
            if email == None or username == None or password_hash == None or role == None or email == "":
                raise errors.MissingFieldError("Email, username, password_hash and role are required.")
    
            if self.exists_registration_request(email):
                raise errors.VerificationError("A registration request with this email already exists.")
    
            self.registration_requests[email] = {
                "code": generate_verification_code(),
                "timestamp": datetime.now(),
                "email": email,
                "username": username,
                "password_hash": password_hash,
                "role": role,
            }
    
            return self.registration_requests[email]["code"]
    
    def add_change_password_request(self, email, new_password) -> str:
                
        if email == None or new_password == None or email == "":
            raise errors.MissingFieldError("Email and new_password are required.")

        if self.exists_change_password_request(email):
            raise errors.VerificationError("A change password request with this email already exists.")

        self.change_password_requests[email] = {
            "code": generate_verification_code(),
            "timestamp": datetime.now(),
            "email": email,
            "new_password": new_password,
        }

        return self.change_password_requests[email]["code"]

    def add_delete_account_request(self, email) -> str:
                                
        if email == None or email == "":
            raise errors.MissingFieldError("Email is required.")

        if self.exists_delete_account_request(email):
            raise errors.VerificationError("A delete account request with this email already exists.")

        self.delete_account_requests[email] = {
            "code": generate_verification_code(),
            "timestamp": datetime.now(),
            "email": email,
        }

        return self.delete_account_requests[email]["code"]  

    def add_reset_password_request(self, email, new_password) -> str:
                                            
            if email == None or new_password == None or email == "" or new_password == "":
                raise errors.MissingFieldError("Email and new_password are required.")
    
            if self.exists_reset_password_request(email):
                raise errors.VerificationError("A reset password request with this email already exists.")
    
            self.reset_password_requests[email] = {
                "code": generate_verification_code(),
                "timestamp": datetime.now(),
                "email": email,
                "new_password": new_password,  
            }
    
            return self.reset_password_requests[email]["code"] 

    def verify_registration_request(self, email, code) -> bool:
        if not self.exists_registration_request(email):
            raise errors.VerificationError("No registration request with this email exists.")
        
        if self.registration_requests[email]["code"] == code:
            from src.models.users import User
            user = User(username=self.registration_requests[email]["username"], email=self.registration_requests[email]["email"], password_hash=self.registration_requests[email]["password_hash"], role=self.registration_requests[email]["role"])
            db.session.add(user)
            db.session.commit()
            del self.registration_requests[email]
            return True
        else:
            return False
        
    def verify_change_password_request(self, email, code) -> bool:
        if not self.exists_change_password_request(email):
            raise errors.VerificationError("No change password request with this email exists.")
        
        if self.change_password_requests[email]["code"] == code:
            from src.models.users import User

            User.query.filter_by(email=email).update(dict(password_hash=self.change_password_requests[email]["new_password"]))
            db.session.commit()
            del self.change_password_requests[email]
            return True
        else:
            return False

    def verify_delete_account_request(self, email, code) -> bool:
        if not self.exists_delete_account_request(email):
            raise errors.VerificationError("No delete account request with this email exists.")
        
        if self.delete_account_requests[email]["code"] == code:
            from src.models.users import User
            User.query.filter_by(email=email).delete()
            db.session.commit()
            del self.delete_account_requests[email]
            return True
        else:
            return False
        
    def verify_reset_password_request(self, email, code) -> bool:
        if not self.exists_reset_password_request(email):
            raise errors.VerificationError("No reset password request with this email exists.")
        
        if self.reset_password_requests[email]["code"] == code:
            from src.models.users import User

            User.query.filter_by(email=email).update(dict(password_hash=self.reset_password_requests[email]["new_password"]))
            db.session.commit()
            del self.reset_password_requests[email]
            return True
        else:
            return False
        
def generate_verification_code() -> str:
        
        """
        Generates a verification code.

        Returns:
            str: The generated verification code.
        """

        return str(random.randint(100000, 999999))

def is_valid_verification_code(code: str) -> bool:
    return code.isnumeric() and len(code) == 6