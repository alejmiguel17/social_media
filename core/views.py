from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Profile, Post, FollowersCount, LikePost #JD 14 08
from django.contrib.auth.decorators import login_required #JD 05 08
from .forms import ProfileUpdateForm
from .models import Follow
import random
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


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



def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    try:
        profile = user.profile
    except ObjectDoesNotExist:
        # Puedes redirigir, mostrar un mensaje, o crear el perfil automáticamente
        return redirect('home')  # o mostrar una página de error personalizada

    posts = Post.objects.filter(user=user).order_by('-created_at')
    return render(request, 'profile.html', {
        'profile_user': user,
        'profile': profile,
        'posts': posts
    })

def logout_view(request):
    logout(request)
    return redirect('index')

#--------------------------------------------
# sistema de publicaciones (post)  #JD 05 08
@login_required(login_url='login')
def upload_post(request):
    if request.method == 'POST':
        user = request.user  # 👈 Esto es el objeto User
        image = request.FILES.get('image_upload')
        caption = request.POST.get('caption')

        new_post = Post.objects.create(user=user, image=image, caption=caption)
        return redirect('posts')

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


@login_required(login_url='login')
def posts_view(request):
    # Usuarios que el usuario actual sigue
    followed_users = User.objects.filter(profile__followers=request.user)
    followed_users = list(followed_users)
    followed_users.append(request.user)

    posts = Post.objects.filter(user__in=followed_users).order_by('-created_at')
    feed_empty = not posts.exists()

    suggestions = User.objects.exclude(id__in=[u.id for u in followed_users])

    context = {
        'posts': posts,
        'feed_empty': feed_empty,
        'suggestions': suggestions,
    }

    return render(request, 'posts.html', context)





@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Comparación directa entre objetos User
    if post.user == request.user or request.user.is_superuser:
        post.delete()

    return redirect('posts')


#--------------------------------------------
@require_POST
@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user

    like_obj, created = LikePost.objects.get_or_create(post=post, user=user)

    if not created:
        like_obj.delete()
        liked = False
    else:
        liked = True

    return JsonResponse({
        'status': 'success',
        'liked': liked,
        'likes_count': LikePost.objects.filter(post=post).count()
    })

def home(request):
    return render(request, 'home.html') 



@login_required
def follow_user(request, user_id):
    if request.method == 'POST':
        try:
            target_user = User.objects.get(id=user_id)
            current_user = request.user

            if current_user == target_user:
                return JsonResponse({'status': 'error', 'message': 'No puedes seguirte a ti mismo'}, status=400)

            # Asumiendo que tienes un modelo Profile con un campo ManyToMany llamado followers
            profile = target_user.profile

            if current_user in profile.followers.all():
                profile.followers.remove(current_user)
                is_following = False
            else:
                profile.followers.add(current_user)
                is_following = True

            followers_count = profile.followers.count()

            return JsonResponse({
                'status': 'success',
                'is_following': is_following,
                'followers_count': followers_count
            })

        except User.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Usuario no encontrado'}, status=404)

    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)

def twita_icon(request):
    if request.method == 'POST':
        # Aquí iría tu lógica para manejar el "twit"
        return JsonResponse({'status': 'success', 'message': 'Twit realizado con éxito'})
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)