from django.urls import path
from .views import (
    PasswordResetConfirmView,
    RegisterView,
    VerifyUserEmailView,
    ResendOTPView,
    LoginUserView,
    LogOutView,
    PasswordResetRequestView,
    GoogleOauthSignInview,
    UserView,
)
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.views import TokenVerifyView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path(
        "confirm-email/<uidb64>/<token>/",
        VerifyUserEmailView.as_view(),
    ),
    path("login/", LoginUserView.as_view(), name="login-user"),
    path("logout/", LogOutView.as_view(), name="blacklist"),
    path("password-reset/", PasswordResetRequestView.as_view(), name="password-reset"),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(),
        name="reset-password-confirm",
    ),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("google/", GoogleOauthSignInview.as_view(), name="google"),
    path("user/", UserView.as_view(), name="user"),
]
