import datetime
from datetime import timedelta
import core.errors as errors
from core.extensions import db
from core.utils.verification import generate_verification_code
from core.utils import emails
from core.models import rejections, users
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

class Verificator:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.registration_requests = {}
            self.scheduler = BackgroundScheduler()
            self.scheduler.add_job(func=self.remove_expired_requests, trigger="interval", seconds=3)
            self.scheduler.start()
            atexit.register(lambda: self.scheduler.shutdown())
            self.initialized = True

    def remove_expired_requests(self):
        current_time = datetime.datetime.now(datetime.timezone.utc)
        five_minutes_ago = current_time - timedelta(minutes=5)

        for user_id, request in list(self.registration_requests.items()):
            if request["timestamp"] < five_minutes_ago:
                del self.registration_requests[user_id]

    def exists_registration_request(self, email: str) -> bool:
        try:
            user = users.get_user_by_email(email)
            return user.id in self.registration_requests
        except errors.UserNotFoundError:
            return False

    def add_registration_request(self, email, username, password_hash, role) -> str:
        if self.exists_registration_request(email):
            if users.is_user_existing_by_email(email):
                del self.registration_requests[users.get_user_by_email(email).id]

        user = users.User(
            username=username, email=email, password_hash=password_hash, role=role
        ) # type: ignore
        db.session.add(user)
        db.session.commit()

        code = generate_verification_code()
        self.registration_requests[user.id] = {
            "code": code,
            "timestamp": datetime.datetime.now(datetime.timezone.utc),
            "failures": 0,
        }

        return code

    def verify_registration_request(self, email, code) -> bool:
        user = users.get_user_by_email(email)
        if not user:
            raise errors.UserNotFoundError("User with this email does not exist.")

        if user.id not in self.registration_requests:
            return False

        request = self.registration_requests[user.id]
        if request["code"] == code:
            user.verification = "done"
            db.session.commit()
            del self.registration_requests[user.id]
            return True
        else:
            request["failures"] += 1
            if request["failures"] > 2:
                del self.registration_requests[user.id]
                users.increase_verification_rejections(email)
            
                if user.verification_rejections > 2:
                    rejections.set_auth_rejection(email)
                    raise errors.VerificationTemporarilyRejectedError(
                        "The user has been temporarily rejected."
                    )
                else:
                    raise errors.VerificationFailureLimitExceededError(
                        "The maximum number of failed attempts has been reached."
                    )

            raise errors.InvalidVerificationCodeError(
                "The verification code is invalid."
            )

    def resend_registration_request(self, email: str) -> None:
        user = users.get_user_by_email(email)
        if not user:
            raise errors.UserNotFoundError("User not found")

        code = generate_verification_code()
        self.registration_requests[user.id] = {
            "code": code,
            "timestamp": datetime.datetime.now(datetime.timezone.utc),
            "failures": 0,
        }

        emails.send_registration_request_email(email, code)

    def has_exceeded_failure_limit(self, email: str) -> bool:
        user = users.get_user_by_email(email)
        if not user:
            raise errors.UserNotFoundError("User not found.")

        return user.verification_rejections > 2