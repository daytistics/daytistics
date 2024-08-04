from core.extensions import db
import datetime
from core.models import users
from core import errors
from core.utils.emails import is_valid_email
from flask import Flask
from core.utils.common import ensure_timezone_aware

SCOPES = ["global", "dashboard", "social", "auth"]

class Rejection(db.Model):
    __tablename__ = "rejections"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    active = db.Column(db.Boolean, default=True)
    scope = db.Column(db.String(255), nullable=False, default="global")
    reason = db.Column(db.String(255), nullable=False)
    ends_at = db.Column(db.DateTime(timezone=True), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.datetime.now(datetime.timezone.utc))

    def __repr__(self):
        return f"<Rejection {self.id} {self.user_id} {self.scope} {self.reason} {self.ends_at} {self.created_at}>"

    
def create_rejection(email: str, reason: str, scope: str = "global", duration_type: str = "s", duration: int = -1) -> Rejection:

    if email is None or email == "" or reason is None or reason == "":
        raise errors.MissingFieldError("Email and reason are required.")
    
    if not is_valid_email(email):
        raise errors.InvalidEmailError("Invalid email.")

    if not users.is_user_existing_by_email(email):
        raise errors.UserNotFoundError("User not found.")
    
    if scope not in SCOPES:
        raise errors.InvalidScopeError("Invalid scope.")

    match duration_type:
        case "y" | "years":
            duration = duration * 60 * 60 * 24 * 365
        case "d" | "days":
            duration = duration * 60 * 60 * 24
        case "h" | "hours":
            duration = duration * 60 * 60
        case "m" | "minutes":
            duration = duration * 60
        case "s" | "seconds":
            pass
        case _:
            raise errors.InvalidDurationTypeError("Invalid duration type.")


    now = datetime.datetime.now(datetime.timezone.utc)
    ends_at = now + datetime.timedelta(seconds=duration)

    rejection = Rejection(
        user_id=users.get_user_by_email(email).id,
        reason=reason,
        scope=scope,
        created_at=now,
        ends_at=ends_at
    ) # type: ignore
    db.session.add(rejection)
    db.session.commit()

    from flask import current_app
    current_app.logger.info(f"Rejection created: {rejection}")
    current_app.logger.info(f"Current time: {now}, Ends at: {ends_at}")

    return rejection

def has_rejection(email: str, scope: str = "global") -> bool:
    
    if not is_valid_email(email):
        raise errors.InvalidEmailError("Invalid email.")
    
    if not users.is_user_existing_by_email(email):
        raise errors.UserNotFoundError("User not found.")

    rejection = Rejection.query.filter_by(user_id=users.get_user_by_email(email).id, scope=scope, active=True).first()
    return rejection is not None

def remove_expired_requests(app: Flask):  
    with app.app_context():
        current_time = datetime.datetime.now(datetime.timezone.utc)
        rejections = Rejection.query.filter(
            Rejection.active == True,
            Rejection.ends_at <= current_time
        ).all()

        for rejection in rejections:
            app.logger.info(f"Removing rejection: {rejection}")
            app.logger.info(f"Current time: {current_time}")
            
            created_at = ensure_timezone_aware(rejection.created_at)
            ends_at = ensure_timezone_aware(rejection.ends_at)
            
            app.logger.info(f"Rejection created at: {created_at}")
            app.logger.info(f"Rejection ends at: {ends_at}")
            app.logger.info(f"Time since creation: {current_time - created_at}")

            user = users.get_user_by_id(rejection.user_id)
            user.verification = "pending"
            user.verification_rejections = 0
            rejection.active = False

        if rejections:
            db.session.commit()
            app.logger.info(f"Removed {len(rejections)} expired rejections")

def set_auth_rejection(email: str):
    create_rejection(email, "Verification rejection", "auth", "s", 10)

    user = users.get_user_by_email(email)
    user.verification = "rejected"
    db.session.commit()

def has_auth_rejection(email: str) -> bool:

    if not is_valid_email(email):
        raise errors.InvalidEmailError("Invalid email.")
    
    if not users.is_user_existing_by_email(email):
        raise errors.UserNotFoundError("User not found.")

    user = users.get_user_by_email(email)
    return user.verification == "rejected" and has_rejection(email, "auth")
