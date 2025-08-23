from django.db import models
from django.contrib.auth.models import User
import uuid #JD 05 08
from datetime import datetime #JD 05 08


# Perfil del usuario
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    followers = models.ManyToManyField(User, related_name='followed_profiles', blank=True)
    bio = models.TextField(blank=True, null=True) #JD 05 08
    # location del usuario
    location = models.CharField(max_length=100, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics', blank=True, null=True)
    
    def __str__(self):
        return self.user.username

#--------------------------------------------
# sistema de publicaciones (post)  #JD 05 08   
class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_images')
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.user.username

    @property
    def likes_count(self):
        return LikePost.objects.filter(post=self).count()
#--------------------------------------------
# sugerencias de usuarios

class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='follows_made', on_delete=models.CASCADE)
    followed = models.ForeignKey(User, related_name='follows_received', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.follower.username} sigue a {self.followed.username}"
    
# sistema de seguimiento
class FollowersCount(models.Model):
    follower = models.CharField(max_length=100)
    following = models.CharField(max_length=100)
    timestamp = models.DateTimeField(default=datetime(2024, 1, 1))  # valor fijo para registros viejos

    def __str__(self):
        return f"{self.follower} sigue a {self.following} el {self.timestamp}"


#--------------------------------------------
# sistema de likes #JD 14 08
class LikePost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} dio like a {self.post.id}"

