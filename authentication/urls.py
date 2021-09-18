from django.urls import reverse, path, include
from .views import RegisterView, VerifyEmail, LoginView,Logout


urlpatterns = [
    path("register/", RegisterView, name="register"),
    path("verify-email/", VerifyEmail, name="verify-email"),
    path("login/", LoginView, name="login"),
    path("logout/", Logout, name="logout"),

]
