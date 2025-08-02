from django.contrib import admin
from django.urls import path
from core.views import index, signup_view, login_view, logout_view, upload_post
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index, name="index"),
    path("signup/", signup_view, name="signup"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path('upload-post/', upload_post, name='upload_post'),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

