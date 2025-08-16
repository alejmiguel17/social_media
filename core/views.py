from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Profile, Post, FollowersCount, LikePost #JD 14 08
from django.contrib.auth.decorators import login_required #JD 05 08
from .forms import ProfileUpdateForm
from django.http import JsonResponse



def index(request):
    if request.user.is_authenticated:
        return redirect('posts')
    error = None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('posts')
        else:
            error = "Usuario o contraseña incorrectos."
    return render(request, 'index.html', {'error': error})

def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        bio = request.POST.get('bio', '')
        location = request.POST.get('location', '')

        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error': 'El nombre de usuario ya existe.'})

        user = User.objects.create_user(username=username, password=password)
        Profile.objects.create(user=user, bio=bio, location=location)
        login(request, user)
        return redirect('index')  

    return render(request, 'signup.html')  


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

        return redirect('posts')
    # else:
    #     return redirect('index')
#--------------------------------------------
# Perfil de usuario y configuración de cuenta
@login_required
def account_settings(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account_settings')
    else:
        form = ProfileUpdateForm(instance=profile)

    return render(request, 'account_settings.html', {'form': form})

# vista de publicaciones en una plantilla posts
from django.contrib.auth.models import User

@login_required(login_url='login')
def posts_view(request):
    user = request.user.username
    following_list = FollowersCount.objects.filter(follower=user).values_list('following', flat=True)
    posts = Post.objects.filter(user__in=following_list).order_by('-created_at')

    feed_empty = not posts.exists()

    # Sugerencias: usuarios que no estás siguiendo y que no eres tú
    all_users = User.objects.exclude(username=user)
    suggestions = all_users.exclude(username__in=following_list)[:5]  # limitar a 5

    return render(request, 'posts.html', {
        'posts': posts,
        'feed_empty': feed_empty,
        'suggestions': suggestions
    })

#--------------------------------------------
def twita_icon(request):
    if request.user.is_authenticated:
        return redirect('posts')
    else:
        return redirect('index')
    
# 
def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)

    # Intenta obtener el perfil, y si no existe, créalo
    profile, created = Profile.objects.get_or_create(user=profile_user)

    is_following = FollowersCount.objects.filter(
        follower=request.user.username,
        following=username
    ).exists()

    user_posts = Post.objects.filter(user=username).order_by('-created_at')

    followers = FollowersCount.objects.filter(following=username).count()
    following = FollowersCount.objects.filter(follower=username).count()

    return render(request, 'profile.html', {
        'profile_user': profile_user,
        'profile': profile,
        'is_following': is_following,
        'user_posts': user_posts,
        'followers': followers,
        'following': following
    })


# sistema de seguimiento
@login_required(login_url='login')
def follow(request):
    if request.method == 'POST':
        follower = request.user
        following_username = request.POST.get('following')
        following = get_object_or_404(User, username=following_username)

        relation = FollowersCount.objects.filter(follower=follower, following=following)

        if relation.exists():
            relation.delete()
            is_following = False
        else:
            FollowersCount.objects.create(follower=follower, following=following)
            is_following = True

        # Nuevo: contar seguidores actualizados
        followers_count = FollowersCount.objects.filter(following=following).count()

        return JsonResponse({
            'is_following': is_following,
            'followers_count': followers_count
        })

    return JsonResponse({'error': 'Método no permitido'}, status=400)


#--------------------------------------------
# sistema de likes  #JD 14 08
@login_required(login_url='signin')
def like_post(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        user = request.user

        post = get_object_or_404(Post, id=post_id)

        like = LikePost.objects.filter(post=post, user=user).first()

        if like:
            like.delete()
            post.no_of_likes -= 1
            is_liked = False
        else:
            LikePost.objects.create(post=post, user=user)
            post.no_of_likes += 1
            is_liked = True

        post.save()

        return JsonResponse({
            'is_liked': is_liked,
            'likes_count': post.no_of_likes
        })

    return JsonResponse({'error': 'Método no permitido'}, status=400)
