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
                "match_type": 2
            },
            "tag_match2": {
                "wrestlers": ["Shane McMahon", "Daniel Bryan", "Kevin Owens", "Sami Zayn"],
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
                "wrestlers": ["The Usos", "The New Day", "The Bludgeon Brothers"],
                "match_type": 5
            },
            "raw_tagteam_championship": {
                "wrestlers": ["The Bar", "Braun Strowman & TBD"],
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
                "match_type": 6
            },
            "andre_the_giant_battle_royale": {
                "wrestlers": ["Dolph Ziggler","Tyler Breeze","Fandango","Woken Matt Hardy","Baron Corbin",
                            "Mojo Rawley","Tye Dillinger","Dash Wilder","Scott Dawson","Goldust","Heath Slater",
                            "Rhyno","Zack Ryder","Primo Colon"],
                "match_type": 6
            }
        }
    }

    # Create event:
    wm34 = insert_event(data["name"], data["date"])
    
    for match_name, match_data in data["matches"].items():
        this_match = insert_match(wm34, match_data["match_type"])
        for wrestler in match_data["wrestlers"]:
            w = insert_wrestler(wrestler)
            # Create link between wrester and match
            link_wrestler_and_match(w, this_match)

def insert_event(name, date):
    print(name,date)
    e = Event.objects.get_or_create(name=name, date=date)[0]
    e.date = date
    e.save()
    return e

def insert_match(event, match_type):
    match = Match(event=event, match_type=match_type)
    match.save()
    return match

def insert_wrestler(name):
    wrestler = Wrestler.objects.get_or_create(name=name)[0]
    return wrestler

def link_wrestler_and_match(wrestler,match):
    wrestler.match.add(match)

if __name__ == '__main__':
    populate()