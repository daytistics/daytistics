import threading
from datetime import datetime, timedelta
import core.errors as errors
import time
from core.extensions import db
from core.utils.verification import generate_verification_code
from core.utils import emails


class Verificator:
    _instance = None

    def __init__(self):
        self.registration_requests = {}
        self.change_password_requests = {}
        self.reset_password_requests = {}
        self.delete_account_requests = {}
        self.change_email_requests = {}
        self._stop_event = threading.Event()
        self._scheduler_thread = threading.Thread(
            target=self._remove_expired_requests_loop
        )
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

        for email, request in list(self.change_email_requests.items()):
            if request["timestamp"] < five_minutes_ago:
                del self.change_email_requests[email]

    def _remove_expired_requests_loop(self):
        while not self._stop_event.is_set():
            self.remove_expired_requests()
            if not self._stop_event.is_set():
                time.sleep(10)

    def stop_scheduler(self):
        self._stop_event.set()
        self._scheduler_thread.join()

    def exists_registration_request(self, email: str) -> bool:
        from core.models import users

        try:
            user = users.get_user_by_email(email)
        except errors.UserNotFoundError:
            return False

        return user.id in self.registration_requests

    def exists_change_password_request(self, email) -> bool:
        from core.models.users import is_user_existing_by_email, get_user_by_email

        if not is_user_existing_by_email(email):
            return False

        user = get_user_by_email(email)

        return user.id in self.change_password_requests

    def exists_reset_password_request(self, email) -> bool:
        from core.models.users import is_user_existing_by_email, get_user_by_email

        if not is_user_existing_by_email(email):
            return False

        user = get_user_by_email(email)

        return user.id in self.reset_password_requests

    def exists_delete_account_request(self, email) -> bool:
        from core.models.users import is_user_existing_by_email, get_user_by_email

        if not is_user_existing_by_email(email):
            return False

        user = get_user_by_email(email)

        return user.id in self.delete_account_requests

    def exists_change_email_request(self, email) -> bool:
        from core.models.users import is_user_existing_by_email, get_user_by_email

        if not is_user_existing_by_email(email):
            return False

        user = get_user_by_email(email)

        return user.id in self.change_email_requests

    def add_registration_request(self, email, username, password_hash, role) -> str:
        from core.models import users

        if self.exists_registration_request(email):
            if users.is_user_existing_by_email(email):
                del self.registration_requests[users.get_user_by_email(email).id]

        user = users.User(
            username=username, email=email, password_hash=password_hash, role=role
        )
        db.session.add(user)
        db.session.commit()

        self.registration_requests[user.id] = {
            "code": generate_verification_code(),
            "timestamp": datetime.now(),
            "failures": 0,
        }

        return self.registration_requests[user.id]["code"]

    def add_change_password_request(self, email, new_password) -> str:
        if email == None or new_password == None or email == "":
            raise errors.MissingFieldError("Email and new_password are required.")

        from core.models.users import get_user_by_email

        user = get_user_by_email(email)

        if self.exists_change_password_request(user.email):
            raise errors.VerificationError(
                "A change password request for this user already exists."
            )

        self.change_password_requests[user.id] = {
            "code": generate_verification_code(),
            "timestamp": datetime.now(),
            "new_password": new_password,
            "failures": 0,
        }

        return self.change_password_requests[user.id]["code"]

    def add_change_email_request(self, current_email, new_email) -> str:
        if (
            current_email == None
            or new_email == None
            or current_email == ""
            or new_email == ""
        ):
            raise errors.MissingFieldError("Current email and new email are required.")

        from core.models.users import get_user_by_email

        user = get_user_by_email(current_email)

        if user.id in self.change_email_requests:
            raise errors.VerificationError(
                "A change email request for this user already exists."
            )

        # Check if the new email is already in use
        from core.models.users import is_user_existing_by_email

        if is_user_existing_by_email(new_email):
            raise errors.EmailInUseError("The new email is already in use.")

        self.change_email_requests[user.id] = {
            "code": generate_verification_code(),
            "timestamp": datetime.now(),
            "new_email": new_email,
            "failures": 0,
        }

        return self.change_email_requests[user.id]["code"]

    def add_delete_account_request(self, email) -> str:
        if email == None or email == "":
            raise errors.MissingFieldError("Email is required.")

        from core.models.users import get_user_by_email

        user = get_user_by_email(email)

        if user.id in self.delete_account_requests:
            raise errors.VerificationError(
                "A delete account request for this user already exists."
            )

        self.delete_account_requests[user.id] = {
            "code": generate_verification_code(),
            "timestamp": datetime.now(),
            "failures": 0,
        }

        return self.delete_account_requests[user.id]["code"]

    def add_reset_password_request(self, email, new_password) -> str:
        if email == None or new_password == None or email == "" or new_password == "":
            raise errors.MissingFieldError("Email and new_password are required.")

        from core.models.users import get_user_by_email

        user = get_user_by_email(email)

        if user.id in self.reset_password_requests:
            raise errors.VerificationError(
                "A reset password request for this user already exists."
            )

        self.reset_password_requests[user.id] = {
            "code": generate_verification_code(),
            "timestamp": datetime.now(),
            "email": email,
            "new_password": new_password,
            "failures": 0,
        }

        return self.reset_password_requests[user.id]["code"]

    def verify_registration_request(self, email, code) -> bool:
        from core.models import users

        if not users.is_user_existing_by_email(email):
            raise errors.UserNotFoundError("User with this email does not exist.")

        if not self.exists_registration_request(email):
            return False

        user = users.get_user_by_email(email)

        if self.registration_requests[user.id]["code"] == code:
            user.verification = "done"
            db.session.commit()

            del self.registration_requests[user.id]
            return True
        else:
            self.registration_requests[user.id]["failures"] += 1

            if user.verification_rejections >= 3:
                from core.extensions import rejector

                rejector.set_submit_code_rejection(email)

                raise errors.TemporarilyRejectedError(
                    "The user has been temporarily rejected."
                )

            if self.registration_requests[user.id]["failures"] >= 3:
                del self.registration_requests[user.id]
                user.verification_rejections += 1
                db.session.commit()
                raise errors.VerificationFailureLimitExceededError(
                    "The maximum number of failed attempts has been reached."
                )

            raise errors.InvalidVerificationCodeError(
                "The verification code is invalid."
            )

    def verify_change_password_request(self, email, code) -> bool:
        from core.models.users import get_user_by_email

        user = get_user_by_email(email)

        if user.id not in self.change_password_requests:
            raise errors.VerificationError(
                "No change password request for this user exists."
            )

        if self.change_password_requests[user.id]["code"] == code:
            from core.models.users import User

            User.query.filter_by(id=user.id).update(
                dict(
                    password_hash=self.change_password_requests[user.id]["new_password"]
                )
            )
            db.session.commit()
            del self.change_password_requests[user.id]
            return True
        else:
            self.change_password_requests[user.id]["failures"] += 1
            if self.change_password_requests[user.id]["failures"] > 3:
                del self.change_password_requests[user.id]
            return False

    def verify_delete_account_request(self, email, code) -> bool:
        from core.models.users import get_user_by_email

        user = get_user_by_email(email)

        if user.id not in self.delete_account_requests:
            raise errors.VerificationError(
                "No delete account request for this user exists."
            )

        if self.delete_account_requests[user.id]["code"] == code:
            from core.models.users import User

            User.query.filter_by(id=user.id).delete()
            db.session.commit()
            del self.delete_account_requests[user.id]
            return True
        else:
            self.delete_account_requests[user.id]["failures"] += 1
            if self.delete_account_requests[user.id]["failures"] > 3:
                del self.delete_account_requests[user.id]
            return False

    def verify_reset_password_request(self, email, code) -> bool:
        from core.models.users import get_user_by_email

        user = get_user_by_email(email)

        if user.id not in self.reset_password_requests:
            raise errors.VerificationError(
                "No reset password request for this user exists."
            )

        if self.reset_password_requests[user.id]["code"] == code:
            from core.models.users import User

            User.query.filter_by(id=user.id).update(
                dict(
                    password_hash=self.reset_password_requests[user.id]["new_password"]
                )
            )
            db.session.commit()
            del self.reset_password_requests[user.id]
            return True
        else:
            self.reset_password_requests[user.id]["failures"] += 1
            if self.reset_password_requests[user.id]["failures"] > 3:
                del self.reset_password_requests[user.id]
            return False

    def verify_change_email_request(self, current_email, code) -> bool:
        from core.models.users import get_user_by_email

        user = get_user_by_email(current_email)

        if user.id not in self.change_email_requests:
            raise errors.VerificationError(
                "No change email request for this user exists."
            )

        if self.change_email_requests[user.id]["code"] == code:
            from core.models.users import User

            new_email = self.change_email_requests[user.id]["new_email"]
            User.query.filter_by(id=user.id).update(dict(email=new_email))
            db.session.commit()
            del self.change_email_requests[user.id]
            return True
        else:
            self.change_email_requests[user.id]["failures"] += 1

            if self.change_email_requests[user.id]["failures"] > 3:
                del self.change_email_requests[user.id]
            return False

    def resend_registration_request(self, email: str) -> None:
        from core.models import users

        if self.exists_registration_request(email):
            if users.is_user_existing_by_email(email):
                del self.registration_requests[users.get_user_by_email(email).id]

        if not users.is_user_existing_by_email(email):
            raise errors.UserNotFoundError("User not found")

        user = users.get_user_by_email(email)

        self.registration_requests[user.id] = {
            "code": generate_verification_code(),
            "timestamp": datetime.now(),
            "failures": 0,
        }

        emails.send_registration_request_email(
            email, self.registration_requests[user.id]["code"]
        )
