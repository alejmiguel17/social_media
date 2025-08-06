from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Profile
from .models import Post #JD 05 08
from django.shortcuts import redirect #JD 05 08
from django.contrib.auth.decorators import login_required #JD 05 08

def index(request):
    return render(request, 'index.html')    

def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        bio = request.POST.get('bio', '')
        location = request.POST.get('location', '')
        user = User.objects.create_user(username=username, password=password)
        Profile.objects.create(user=user, bio=bio, location=location)
        login(request, user)
        return redirect('index')
    return render(request, 'signup.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('index')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('index')

#--------------------------------------------
# sistema de publicaciones (post)  #JD 05 08
@login_required(login_url='login') 
def upload_post(request):
    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST.get('caption')

        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()

        return redirect('index')
    else:
        return redirect('index')
#--------------------------------------------