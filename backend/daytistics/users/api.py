# from django.http import HttpResponse
# from django.shortcuts import render
# from requests import Response
# from rest_framework.views import APIView
# from django.core.mail import EmailMessage
# from django.template.loader import render_to_string
# from django.contrib.sites.shortcuts import get_current_site
# from django.utils.http import urlsafe_base64_encode
# from django.utils.encoding import force_bytes
# from daytistics.users.models import CustomUser
# from django.shortcuts import redirect
# from django.utils.encoding import force_str
# from django.utils.http import urlsafe_base64_decode
# from django.contrib.auth import get_user_model
# from django.contrib.auth.models import User
# from .tokens import account_activation_token
# from daytistics.utils.validation import is_valid_email, is_valid_username, is_valid_password
# from daytistics.utils.api import success_response, error_response
# from rest_framework_simplejwt.authentication import JWTAuthentication
# from rest_framework_simplejwt.tokens import RefreshToken, OutstandingToken
# from .serializers import CustomUserSerializer
# from django.utils import timezone


# class CheckAuthView(APIView):
#     authentication_classes = [JWTAuthentication]

#     def get(self, request):
#         return success_response({'message': 'You are authenticated!'}, 200)

# class DataView(APIView):
#     authentication_classes = [JWTAuthentication]

#     def get(self, request):
#         serializer = CustomUserSerializer(request.user)
#         return success_response(serializer.data, 200)

from django.core.mail import EmailMessage
from django.conf import settings
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import get_user_model
from django.utils import timezone
from ninja import Router
from ninja_jwt.tokens import RefreshToken
from ninja_jwt.authentication import JWTAuth

from .tokens import account_activation_token
from .schemes import (
    UserRegisterRequest,
    UserLoginRequest,
    JwtTokensResponse,
    UserProfileResponse,
)
from ..activities.models import ActivityType
from ..utils.schemes import Message
from ..users.models import CustomUser
from ..utils.validation import (
    is_valid_email,
    is_valid_username,
    is_valid_password,
)

router = Router()


@router.get("/activate/{uidb64}/{token}", response={200: Message, 400: Message})
def activate(request, uidb64: str, token: str):
    User = get_user_model()

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        return 200, {"detail": "Account activated successfully!"}
    else:
        return 400, {"detail": "Activation link is invalid."}


@router.post("register", response={201: Message, 400: Message})
def register(request, data: UserRegisterRequest):
    def _send_verification_email(user):
        mail_subject = "Activate your user account."
        message = render_to_string(
            "emails/account_activation.html",
            {
                "username": user.username,
                "domain": settings.FRONTEND_URL,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": account_activation_token.make_token(user),
                "protocol": "https" if request.is_secure() else "http",
            },
        )
        email = EmailMessage(mail_subject, message, to=[user.email])
        email.send()

    username = data.username
    email = data.email
    password1 = data.password1
    password2 = data.password2

    if not is_valid_username(username):
        return 400, {"detail": "Invalid username."}

    if not is_valid_email(email):
        return 400, {"detail": "Invalid email."}

    if CustomUser.objects.filter(email=email).exists():
        return 400, {"detail": "User already exists."}

    if not is_valid_password(password1):
        return 400, {"detail": "Invalid or insecure password."}

    if password1 != password2:
        return 400, {"detail": "Passwords do not match."}

    user = CustomUser.objects.create_user(
        username=username, email=email, password=password1, is_active=False
    )

    user.activities.set(ActivityType.objects.all())
    user.save()

    _send_verification_email(user)

    return 201, {"detail": "Please check your email to verify your account."}


@router.post("login", response={200: JwtTokensResponse, 400: Message, 404: Message})
def login(request, data: UserLoginRequest):
    email = data.email
    password = data.password

    if email is None or password is None or email == "" or password == "":
        return 400, {"detail": "Email and password are required."}

    if not is_valid_email(email):
        return 400, {"detail": "Invalid email."}

    if not CustomUser.objects.filter(email=email).exists():
        return 404, {"detail": "User not found."}

    user = CustomUser.objects.get(email=email)

    if not user.is_active:
        return 400, {"detail": "Account is not activated."}

    if user.check_password(password):
        user.last_login = timezone.now()
        user.save(update_fields=["last_login"])

        refresh = RefreshToken.for_user(user)
        return 200, {
            "accessToken": str(refresh.access_token),
            "refreshToken": str(refresh),
        }

    return 400, {"detail": "Invalid credentials."}


@router.get("/profile", response={200: UserProfileResponse}, auth=JWTAuth())
def get_user_profile(request):
    user = request.user
    profile = {
        "username": user.username,
        "email": user.email,
        "is_active": user.is_active,
        "is_staff": user.is_staff,
        "is_superuser": user.is_superuser,
        "groups": [group.name for group in user.groups.all()],
        "user_permissions": [
            permission.codename for permission in user.user_permissions.all()
        ],
        "date_joined": user.date_joined,
        "last_login": user.last_login,
        "date_format": user.date_format,
    }

    return 200, profile
