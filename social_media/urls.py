from django.contrib import admin
from django.urls import path
from core.views import index, signup_view, login_view, logout_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index, name="index"),
    path("signup/", signup_view, name="signup"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
]