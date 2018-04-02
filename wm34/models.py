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


class Event(models.Model):    
    name = models.CharField(max_length=128)
    date = models.DateTimeField(default=None)
    user = models.ManyToManyField(User, through="UserEvent")


class UserEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    points = IntegerField(default=0)


class Match(models.Model):

    event = models.ForeignKey(Event)

    # Game types take the following values in order to reference integer field:
    SINGLE = 1
    TAG = 2
    TRIPLE = 3
    FOUR = 4
    TRIPLE_TAG = -5
    ROYALE = 6
    LADDER = 7
    TABLE = 8

    MATCH_CHOICES = (
        (SINGLE, "Singles"),
        (TAG, "Tag Team"),
        (TRIPLE< "Triple Threat"),
        (FOUR, "Fatal Four-way"),
        (TRIPLE_TAG, "Triple Threat Tag Team"),
        (ROYALE, "Battle Royale"),
        (LADDER, "Ladder"),
        (TABLE, "Tables"),
    )

    elimination = models.BooleanField(default=False)
    match_type = models.IntegerField(choices=MATCH_CHOICES, default=SINGLE)


class Wrestler(models.Model):
    name = models.CharField(max_length=128)
    match = models.ManyToManyField(Match)

