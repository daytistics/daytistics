from django.http import HttpResponse
from django.shortcuts import render
from requests import Response
from rest_framework.views import APIView
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from app.accounts.models import CustomUser
from django.shortcuts import redirect
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from .tokens import account_activation_token
from app.utils.validation import is_valid_email, is_valid_username, is_valid_password
from app.utils.api import success_response, error_response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken, OutstandingToken
from .serializers import CustomUserSerializer
from django.utils import timezone

class RegisterView(APIView):
    def post(self, request):

        print(request.data)

        body = request.data
        username = body.get('username')
        email = body.get('email')
        password = body.get('password1')

        if not is_valid_username(username):
            return error_response('Invalid username.', 400)

        if not is_valid_email(email):
            return error_response('Invalid email.', 400)

        if not is_valid_password(password):
            return error_response('Invalid password.', 400)

        if CustomUser.objects.filter(username=username).exists():
            return error_response('Username already exists.', 400)


        user = CustomUser.objects.create_user(
         username=username, email=email, password=password, is_active=False
        )

        self._send_verification_email(user)

        return HttpResponse('Please check your email to verify your account.', status=201)

    def _send_verification_email(self, user):
        mail_subject = 'Activate your user account.'
        message = render_to_string(
         'emails/account_activation.html',
         {
          'username': user.username,
          'domain': get_current_site(self.request).domain,
          'uid': urlsafe_base64_encode(force_bytes(user.pk)),
          'token': account_activation_token.make_token(user),
          'protocol': 'https' if self.request.is_secure() else 'http',
         },
        )
        email = EmailMessage(mail_subject, message, to=[user.email])
        email.send()


class AccountActivationView(APIView):
    def get(self, request, uidb64, token):
        User = get_user_model()

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()

            return HttpResponse('Account activated successfully!', status=600)
        else:
            return HttpResponse('Activation link is invalid!', status=604)


class LoginView(APIView):

    def post(self, request):
        body = request.data
        email = body.get('email')
        password = body.get('password')

        user = CustomUser.objects.get(email=email)

        if user is not None and user.check_password(password):
            user.last_login = timezone.now()
            refresh = RefreshToken.for_user(user)
            return success_response(
                {
                    'accessToken': str(refresh.access_token),
                    'refreshToken': str(refresh),
                }, 200)

        return error_response('Invalid credentials.', 401)  #

class CheckAuthView(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        return success_response({'message': 'You are authenticated!'}, 200)

class DataView(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        serializer = CustomUserSerializer(request.user)
        return success_response(serializer.data, 200)
