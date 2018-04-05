import os, sys
from datetime import datetime

# Set up project environment
proj_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wrestlemania.settings")
sys.path.append(proj_path)
os.chdir(proj_path)

# Ensure models get loaded.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# Import all models
from wm34.models import *


def populate():

    data = {
        "name": "Wrestlemania 34",
        "date": "2018-04-08 19:00",
        "matches": {
            "universal_championship": {
                "wrestlers": ["Brock Lesnar", "Roman Reigns"],
                "match_type": 1
            },
            "wwe_championship": {
                "wrestlers": ["AJ Styles", "Shinsuke Nakamura"],
                "match_type": 1
            },
            "tag_match": {
                "wrestlers": ["Ronda Rousey", "Kurt Angle", "Stephanie McMahon", "Triple H"],
                "teams": {"Ronda Rousey & Kurt Angle": ["Ronda Rousey", "Kurt Angle"], 
                          "Stephanie McMahon & Triple H": ["Stephanie McMahon", "Triple H"]
                         },
                "match_type": 2
            },
            "tag_match2": {
                "wrestlers": ["Shane McMahon", "Daniel Bryan", "Kevin Owens", "Sami Zayn"],
                "teams": {"Shane McMahon & Daniel Bryan": ["Shane McMahon", "Daniel Bryan"], 
                          "Kevin Owens & Sami Zayn": ["Kevin Owens", "Sami Zayn"]
                         },
                "match_type": 2
            },
            "smackdown_womens_championship": {
                "wrestlers": ["Charlotte Flair", "Asuka"],
                "match_type": 1
            },
            "raw_womens_championship": {
                "wrestlers": ["Alexa Bliss", "Nia Jax"],
                "match_type": 1
            },
            "intercontinental_championship": {
                "wrestlers": ["The Miz", "Seth Rollins", "Finn Balor"],
                "match_type": 3
            },
            "united_states_championship": {
                "wrestlers": ["Randy Orton", "Bobby Roode", "Jinder Mahal", "Rusev"],
                "match_type": 4
            },
            "smackdown_tagteam_championship": {
                "wrestlers": ["Jey Uso", "Jimmy Uso", "Big E", "Kofi Kingston", "Xavier Woods", "Luke Harper", "Eric Rowan"],
                "teams": {"The Usos": ["Jey Uso", "Jimmy Uso"], 
                          "The New Day": ["Big E", "Kofi Kingston", "Xavier Woods"],
                          "The Bludgeon Brothers": ["Luke Harper", "Eric Rowan"]
                          },
                "match_type": 5
            },
            "raw_tagteam_championship": {
                "wrestlers": ["Cesaro", "Sheamus", "Braun Strowman"],
                "teams": {"The Bar": ["Cesaro", "Sheamus"], 
                          "Braun Strowman & TBD": ["Braun Strowman",]
                          },
                "match_type": 2
            },
            "cruiserweight_championship": {
                "wrestlers": ["Cedric Alexander", "Mustafa Ali"],
                "match_type": 1
            },
            "taker_cena": {
                "wrestlers": ["Undertaker", "John Cena"],
                "match_type": 1
            },
            "womens_battle_royal": {
                "wrestlers": ["Bayley", "Sasha Banks","Ruby Riott","Sarah Logan","Liv Morgan","Becky Lynch","Naomi","Natalya","Lana","Mickie James","Mandy Rose","Sonya Deville","Carmella"], 
                "match_type": 6,
                "name": "WrestleMania Women's Battle Royal"
            },
            "andre_the_giant_battle_royal": {
                "wrestlers": ["Dolph Ziggler","Tyler Breeze","Fandango","Woken Matt Hardy","Baron Corbin",
                            "Mojo Rawley","Tye Dillinger","Dash Wilder","Scott Dawson","Goldust","Heath Slater",
                            "Rhyno","Zack Ryder","Primo Colon"],
                "match_type": 6,
                "name": "Andre the Giant Battle Royal"
            }
        }
    }

    # Create event:
    wm34 = insert_event(data["name"], data["date"])
    
    for match_name, match_data in data["matches"].items():
        try:
            this_match = insert_match(wm34, match_data["match_type"], match_data["name"])
        except KeyError:
            this_match = insert_match(wm34, match_data["match_type"])
        for wrestler in match_data["wrestlers"]:
            w = insert_wrestler(wrestler)
            # Create link between wrester and match
            link_wrestler_and_match(w, this_match)
        try:
            for team, wrestlers in match_data["teams"].items():
                t = insert_team(team)
                # Create link between team and wrestlers
                for w in wrestlers:
                    link_wrestler_and_team(w, t)
                # Create link between team and match
                link_team_and_match(t, this_match)
        except KeyError:
            pass
        


def insert_event(name, date):
    print(name,date)
    e = Event.objects.get_or_create(name=name, date=date)[0]
    e.date = date
    e.save()
    return e

def insert_wrestler(name):
    wrestler = Wrestler.objects.get_or_create(name=name)[0]
    return wrestler

def insert_team(name):
    team = Team.objects.get_or_create(name=name)[0]
    return team

def insert_match(event, match_type, name=""):
    match = Match(event=event, match_type=match_type, name=name)
    match.save()
    return match

def link_wrestler_and_team(wrestler,team):
    w = Wrestler.objects.get_or_create(name=wrestler)[0]
    t = Team.objects.get_or_create(name=team)[0]
    w.team.add(t)

def link_wrestler_and_match(wrestler,match):
    match.wrestler.add(wrestler)

def link_team_and_match(team,match):
    match.team.add(team)

if __name__ == '__main__':
    populate()