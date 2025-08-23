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
from core import views
from core.views import like_post
from uuid import UUID

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup_view, name='signup'),
    path('logout', views.logout_view, name='logout'),
    path('upload-post', views.upload_post, name='upload-post'),
    path('posts', views.posts_view, name='posts'),  # JD 05 08
    path('account/settings/', views.account_settings, name='account_settings'),
    path('home', views.home, name='home'),
    path('follow/<int:user_id>/', views.follow_user, name='follow_user'),
    path('twita/', views.twita_icon, name='twita_icon'),
    path('like/<uuid:post_id>/', views.like_post, name='like_post'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('delete_post/<uuid:post_id>/', views.delete_post, name='delete_post'),
    path('mi-perfil/', views.my_profile, name='my_profile'),
    path('follow-toggle/', views.follow_toggle, name='follow-toggle'),
    path('delete-account/', views.delete_account, name='delete_account'),

]
#--------------------------------------------