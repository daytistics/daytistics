from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import api

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
	path('register/', api.RegisterView.as_view(), name='register'),
	path('activate/<uidb64>/<token>', api.AccountActivationView.as_view(), name='activate'),
	path('login/', api.LoginView.as_view(), name='login'),
	path('auth/', api.CheckAuthView.as_view(), name='auth'),
	path('data/', api.DataView.as_view(), name='data'),
]
