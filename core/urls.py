#from django.contrib import admin
#from django.urls import path, include
#from . import views  #JD 05 08
#
#urlpatterns = [
#    path('admin/', admin.site.urls),
#    path('', include('core.urls')),
#    path('upload-post', views.upload_post, name='upload-post'), #JD 05 08
#]

# core/urls.py

# core/urls.py

#--------------------------------------------
# sistema de publicaciones (post)  #JD 05 08
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup_view, name='signup'),
    path('logout', views.logout_view, name='logout'),
    path('upload-post', views.upload_post, name='upload-post'),
    path('posts', views.posts_view, name='posts'),  # JD 05 08
    path('account/settings/', views.account_settings, name='account_settings')
]
#--------------------------------------------