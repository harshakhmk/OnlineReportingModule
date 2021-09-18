from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from .models import User
from django.contrib.auth import logout
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from utils.email import Util
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status, generics, views

# Create your views here.


def home(request):
    if request.user.is_authenticated:
        return render(request, "auth.html")
    return render(request, "unauth.html")


def RegisterView(request):
    if request.method == "GET":
        form = RegisterForm()
        return render(request, "signup.html", {"form": form})
    else:
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user = User.objects.get(email=form.get("email",""))
            token = RefreshToken.for_user(user).access_token
            current_domain = get_current_site(request).domain
            relative_url = reverse("verify-email")
            absolute_url = (
            "http://" + current_domain + relative_url + "?token=" + str(token)
            )
            message_body = (
            f"Hi {user.username}, please verify your email address from below link\n"
            + absolute_url
        )
            email_data = {
            "body": message_body,
            "subject": "Verify your email",
            "to_email": user.email,
        }
            Util.send_email(email_data)
            messages.success(request, "Your account successfully created")
            return redirect("login")
        else:
            messages.error(request, "Invalid data")
            return redirect("register")


def VerifyEmail(request):
    token = request.GET.get("token")
    try:
            data = jwt.decode(token, settings.SECRET_KEY)
            user = User.objects.filter(id=data["user_id"])
            message = ""
            if user.is_verified:
                message =  "Already verified"

            user.is_verified = True
            user.save()
            message = "Successfully verified"
            messages.success(request, f" {message} ")
            return
    except jwt.ExpiredSignatureError as e:
                message="Activation link Expired"

    except jwt.Exceptions.DecodeError as de:
            message= "Invalid Token"
    messages.error(request, f"{message} ")
    return redirect("verify-email")


def Logout(request):

    logout(request)
    messages.success(request, "You have been logged out")
    return redirect("/")


def LoginView(request):
    if request.method == "GET":
        f = LoginForm()
        return render(request, "login.html", {"form": f})
    elif request.method == "POST":
        f = LoginForm(request.POST)
        if f.is_valid():

            user = auth.authenticate(
                email=request.POST.get("email"), password=request.POST.get("password")
            )
            if user is not None:  # valid user
                auth.login(request, user)
                messages.success(request, "You have been Loged in")
                return redirect("/")

        messages.info(request, "invalid username or password")
        return redirect("login")
