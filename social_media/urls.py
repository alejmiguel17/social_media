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
from core import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#--------------------------------------------