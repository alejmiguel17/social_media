from django.db import models
from django.contrib.auth.models import User

# profile.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True)
    

    def __str__(self):
        return self.user.username
    
