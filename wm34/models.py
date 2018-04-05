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

    # Override the __str__() method.
    def __str__(self):
        return self.name


class Team (models.Model):
    name = models.CharField(unique=True, max_length=128)

    # Override the __str__() method.
    def __str__(self):
        return self.name


class Wrestler(models.Model):
    name = models.CharField(unique=True, max_length=128)
    team = models.ManyToManyField(Team, blank=True)

    # Override the __str__() method.
    def __str__(self):
        return self.name


class Match(models.Model):

    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    name = models.CharField(max_length=128, blank=True)

    # Game types take the following values in order to reference integer field:
    SINGLE = 1
    TAG = 2
    TRIPLE = 3
    FOUR = 4
    TRIPLE_TAG = 5
    ROYALE = 6
    LADDER = 7
    TABLE = 8

    MATCH_CHOICES = (
        (SINGLE, "Singles"),
        (TAG, "Tag Team"),
        (TRIPLE, "Triple Threat"),
        (FOUR, "Fatal Four-way"),
        (TRIPLE_TAG, "Triple Threat Tag Team"),
        (ROYALE, "Battle Royale"),
        (LADDER, "Ladder"),
        (TABLE, "Tables"),
    )
    match_type = models.IntegerField(choices=MATCH_CHOICES, default=SINGLE)

    wrestler = models.ManyToManyField(Wrestler)
    team = models.ManyToManyField(Team, blank=True)


    class Meta:
        verbose_name_plural = "Matches"

    # Override the __str__() method.
    def __str__(self):
        if self.name:
            return "%s: %s" % (str(self.event), self.name)
        elif self.team.all():
            teams = " vs. ".join(str(t) for t in self.team.all())
            return "%s: %s" % (str(self.event), teams)
        else:
            wrestlers = " vs. ".join(str(w) for w in self.wrestler.all())
            return "%s: %s" % (str(self.event), wrestlers)


class UserEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "User Event [Join]"


class UserMatchAnswers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "User Match Answers"

    ###########################################################
    ### FOR ALL MATCH TYPES
    # Winner of the match - 5 points.
    winner = models.CharField(max_length=128)
    
    ## If method is determined by match-type, then gimmick is used instead - 2 points.
    # Method of victory.
    METHOD_CHOICES = (
        (1, "Pin"),
        (2, "Submission"),
        (3, "Disqualification"),
    )
    method = models.IntegerField(choices=METHOD_CHOICES, default=1)
    # Gimmick match (ladder, steel cage, etc.) - selects wrestler who does first ... of the match.
    gimmick = models.CharField(max_length=128)
    
    # Duration of match, categorised - 2 points.
    DURATION_CHOICES = (
        (1, "0 - 4:59"),
        (2, "5 - 9:59"),
        (3, "10 - 14:59"),
        (4, "15 - 19:59"),
        (5, "20 - 24:59"),
        (6, "25 - 29:59"),
        (7, "30+"),
    )
    duration = models.IntegerField(choices=DURATION_CHOICES, default=1)

    # Interference in the match? 1 point.
    interference = models.BooleanField(default=False)


    ###########################################################
    ### MATCH-TYPE SPECIFIC - Only fill one block per match
    
    ## Normal match.
    finishers = models.IntegerField(default=0) # 2 points
    table_used = models.BooleanField(default=False) # 1 points
    injury = models.BooleanField(default=False) # 1 points
    ref_comatose = models.BooleanField(default=False) # 1 points

    ## Multi-man/tag-team matches.
    who_pins = models.CharField(max_length=128) # 2 points
    who_pinned = models.CharField(max_length=128) # 2 points
    heel_turn = models.BooleanField(default=False) # 1 points    

    ## Battle Royale
    first_out = models.CharField(max_length=128) # 1 point
    final_four_one = models.CharField(max_length=128) # 1 point
    final_four_two = models.CharField(max_length=128) # 1 point
    final_four_three = models.CharField(max_length=128) # 1 point
    final_four_four = models.CharField(max_length=128) # 1 point
