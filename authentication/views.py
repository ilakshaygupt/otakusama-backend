import random
from django.conf import settings
import requests
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response


from authentication.models import User

from rest_framework_simplejwt.authentication import JWTAuthentication

from authentication.serializers import (
    RegisterSerializer,
    ResendOTPSerializer,
    SetNewPasswordSerializer,
    VerifyEmailSerializer,
    LoginSerializer,
    LogoutUserSerializer,
    GoogleSignInSerializer,
    PasswordResetRequestSerializer,
    UserSerializer,
)
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from authentication.utils import random_password, send_generated_otp_to_email
from django.contrib.auth import authenticate
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import smart_str
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
import hashlib


class RegisterView(GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializers = self.serializer_class(data=request.data)
        serializers.is_valid(raise_exception=True)

        user = User.objects.filter(email=serializers.validated_data["email"])

        if user and user[0].is_verified:
            return Response(
                {"message": "email already exists", "success": False},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user.delete()
        user = User.objects.filter(username=serializers.validated_data["username"])

        if user and user[0].is_verified:
            return Response(
                {"message": "username already exists", "success": False},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user.delete()

        user = serializers.save()
        uidb64 = urlsafe_base64_encode(smart_str(user.id).encode())
        token = PasswordResetTokenGenerator().make_token(user)
        email_subject = "Password Reset Request"
        current_site = get_current_site(request).domain
        abslink = f"https://${current_site}/auth/confirm-email/{uidb64}/{token}/"
        email_body = (
            f"Hi {user.username}, use the link below to reset your password: {abslink}"
        )
        from_email = settings.EMAIL_HOST_USER
        d_email = EmailMessage(
            subject=email_subject,
            body=email_body,
            from_email=from_email,
            to=[user.email],
        )
        d_email.send()
        return Response(
            {
                "success": True,
                "message": "An email to verify your caccent has been succesfully send to your Gmail",
            },
            status=status.HTTP_200_OK,
        )


class VerifyUserEmailView(GenericAPIView):
    serializer_class = VerifyEmailSerializer

    def get(self, request, uidb64, token):
        serializer = self.serializer_class(
            data=request.data, context={"uidb64": uidb64, "token": token}
        )
        serializer.is_valid(raise_exception=True)
        id = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(id=id)
        user.is_verified = True
        user.save()
        return Response(
            {"message": "ACcount verified successufully", "success": True},
            status=status.HTTP_200_OK,
        )


class LoginUserView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]
        try:
            user = User.objects.get(email=email)
        except:
            return Response(
                {"message": "Email doesn't exist", "success": False},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not user.is_verified:
            return Response(
                {"message": "Email is not verifies", "success": False},
                status=status.HTTP_400_BAD_REQUEST,
            )
        tokens = user.tokens()

        user = authenticate(request, email=email, password=password)
        if not user:
            return Response(
                {"message": "Email and Password doesn't match", "success": False},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {
                "message": "Logged in successfully",
                "access_token": str(tokens["access"]),
                "refresh_token": str(tokens["refresh"]),
                "success": True,
                "username": user.username,
                "email": user.email,
            },
            status=status.HTTP_200_OK,
        )


class LogOutView(GenericAPIView):
    serializer_class = LogoutUserSerializer

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        refresh_token = serializer.validated_data["refresh_token"]
        try:
            refresh_token = RefreshToken(refresh_token)
            refresh_token.blacklist()
        except TokenError:
            return Response(
                {"message": "Token is invalid or expired", "success": False},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {"message": "Logged out successfully", "success": True},
            status=status.HTTP_200_OK,
        )


class ResendOTPView(GenericAPIView):
    serializer_class = ResendOTPSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        try:
            user = User.objects.get(email=email)
        except:
            return Response(
                {"message": "Email doesn't exist", "success": False},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not user.is_verified:
            send_generated_otp_to_email(email, request)
            return Response(
                {"message": "OTP resend successfully", "success": True},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"message": "Email is already verified", "success": False},
                status=status.HTTP_400_BAD_REQUEST,
            )


class GoogleOauthSignInview(GenericAPIView):
    serializer_class = GoogleSignInSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        authorization_token = serializer.validated_data["access_token"]
        url = f"https://www.googleapis.com/oauth2/v3/userinfo?access_token={authorization_token}"
        response = requests.get(url)
        if response.status_code == 200:
            user_data = response.json()
            print(user_data)
        try:
            user_data["sub"]
        except:
            return Response(
                {
                    "message": "this token has expired or invalid please try again",
                    "success": False,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            user = User.objects.get(email=user_data["email"])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            tokens = user.tokens()
            return Response(
                {
                    "message": "Signed successfully",
                    "access_token": str(tokens["access"]),
                    "refresh_token": str(tokens["refresh"]),
                    "success": True,
                },
                status=status.HTTP_200_OK,
            )
        except:
            provider = "google"
            family_name = user_data.get("family_name", "")
            base_username = f"{user_data['given_name'].lower()}.{family_name.lower()}"
            username = base_username
            username = hashlib.sha256(str(user.id).encode()).hexdigest()
            counter = 1
            while User.objects.filter(username=username).exists():
                username = hashlib.sha256((str(user.id) + str(counter)).encode()).hexdigest()
                counter += 1
            new_user = {
                "email": user_data["email"],
                "username": username,
                "password": random_password(),
            }
            user = User.objects.create_user(**new_user)
            user.auth_provider = provider
            user.is_verified = True
            user.save()
            tokens = user.tokens()
            return Response(
                {
                    "message": "account created successfully",
                    "access_token": str(tokens["access"]),
                    "refresh_token": str(tokens["refresh"]),
                    "success": True,
                },
                status=status.HTTP_201_CREATED,
            )


class UserView(GenericAPIView):
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        serializer = self.serializer_class(request.user)

        return Response(
            {
                "email": serializer.data["email"],
                "username": serializer.data["username"],
                "success": True,
            },
            status=status.HTTP_200_OK,
        )


class PasswordResetRequestView(GenericAPIView):
    serializer_class = PasswordResetRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        try:
            user = User.objects.get(email=email)
        except:
            return Response(
                {"message": "Email is not registered", "success": False},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not user.is_verified:
            return Response(
                {"message": "Email is not verified", "success": False},
                status=status.HTTP_400_BAD_REQUEST,
            )
        uidb64 = urlsafe_base64_encode(smart_str(user.id).encode())
        token = PasswordResetTokenGenerator().make_token(user)
        email_subject = "Password Reset Request"
        current_site = get_current_site(request).domain
        abslink = f"http://localhost:3000/login/reset_password/{uidb64}/{token}/"
        email_body = (
            f"Hi {user.username}, use the link below to reset your password: {abslink}"
        )
        from_email = settings.EMAIL_HOST_USER
        d_email = EmailMessage(
            subject=email_subject,
            body=email_body,
            from_email=from_email,
            to=[user.email],
        )
        d_email.send()
        return Response(
            {
                "success": True,
                "message": "An email to reset psasword has been sent to your email.",
            },
            status=status.HTTP_200_OK,
        )


class PasswordResetConfirmView(GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def post(self, request, uidb64, token):
        serializer = self.serializer_class(
            data=request.data, context={"uidb64": uidb64, "token": token}
        )
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data["password"]
        id = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(id=id)
        if not PasswordResetTokenGenerator().check_token(user, token):
            return Response(
                {"message": "The reset link is invalid", "success": False},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        user.set_password(password)
        user.save()
        return Response(
            {"message": "Password reset successfully", "success": True},
            status=status.HTTP_200_OK,
        )
