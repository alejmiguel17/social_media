from django.db import models
from django.contrib.auth.models import User
import uuid #JD 05 08
from datetime import datetime #JD 05 08

# profile.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True)
    

    def __str__(self):
        return self.user.username

#--------------------------------------------
# sistema de publicaciones (post)  #JD 05 08   
class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    image = models.ImageField(upload_to='post_images')
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    no_of_likes = models.IntegerField(default=0)

    def __str__(self):
        return self.user
#--------------------------------------------