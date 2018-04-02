from django.db import models

from django.contrib import admin
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

class UserProfile(models.Model):
    # This line is required. Link UserProfile to a User model instance.
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    #The additional attributes we wish to include.
    picture = models.ImageField(upload_to='profile_images', blank=True)

    #Override the __unicode__() method to return out something meaningful!
    def __str__(self):
        return self.user.username