from django.contrib import admin
from wm34.models import Event, Match, Wrestler, Team, UserEvent, UserMatchAnswers 

admin.site.register(Event)
admin.site.register(Match)
admin.site.register(Wrestler)
admin.site.register(Team)
admin.site.register(UserEvent)
admin.site.register(UserMatchAnswers)