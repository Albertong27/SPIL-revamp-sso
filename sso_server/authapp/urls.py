# sso_server/authapp/urls.py
from django.urls import path
from . import views
from django.conf.urls import include

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("validate/", views.validate_token, name="validate"),
]
