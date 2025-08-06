#from django.contrib import admin
#from django.urls import path, include #JD 05 08
#from core.views import index, signup_view, login_view, logout_view
#
#urlpatterns = [
#    path("admin/", admin.site.urls),
#    path("", index, name="index"),
#    path("signup/", signup_view, name="signup"),
#    path("login/", login_view, name="login"),
#    path("logout/", logout_view, name="logout"),
#    path('' , include('core.urls')),  #JD 05 08
#]


# social_media/urls.py

#--------------------------------------------
# sistema de publicaciones (post)  #JD 05 08
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
]
#--------------------------------------------