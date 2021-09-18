from rest_framework import serializers
from .models import User
from rest_framework.exceptions import AuthenticationFailed
from django.contrib import auth

# from django.contrib.auth.token import PasswordResetTokenGenerator
from django.utils.encoding import (
    force_str,
    smart_str,
    smart_bytes,
    DjangoUnicodeDecodeError,
)
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from utils.email import Util
from django.urls import reverse



class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=60, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ["email", "username", "password"]

    # This function runs when is_valid() is invoked
    def validate(self, attrs):
        username = attrs.get("username", "")
        email = attrs.get("email", "")

        if not username.isalnum():
            raise ValidationError(
                "user name must contain alpha numeric characters only"
            )

        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=500)

    class Meta:
        model = User
        fields = "token"


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=100, min_length=10)
    password = serializers.CharField(max_length=100, min_length=8, write_only=True)
    username = serializers.CharField(max_length=100, min_length=5, read_only=True)
    tokens = serializers.CharField(max_length=500, read_only=True)

    class Meta:
        model = User
        fields = ("email", "password", "username", "tokens")

    def validate(self, attrs):
        email = attrs.get("email", "")
        password = attrs.get("password", "")

        user = auth.authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed("Invalid Creds")
        if user.is_verified == False:
            AuthenticationFailed("Email not verified")
        return {
            "email": user.email,
            "username": user.username,
            "tokens": user.tokens(),
        }


