from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Profile, Post
from django.contrib.auth.decorators import login_required
from .forms import PostForm

def index(request):
    form = PostForm()
    return render(request, 'index.html', {'form': form})


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

@login_required
def upload_post(request):
    if request.method == 'POST':
        caption = request.POST.get('caption')
        image = request.FILES.get('image')

        if image:
            Post.objects.create(
                user=request.user,
                caption=caption,
                image=image
            )
            return redirect('index')
        else:
            return render(request, 'upload_post.html', {
                'error': 'Debes subir una imagen.'
            })

    return render(request, 'upload_post.html')

from .models import Post

def home(request):
    posts = Post.objects.all().order_by('-created_at')  # O cualquier orden que uses
    return render(request, 'home.html', {'posts': posts})