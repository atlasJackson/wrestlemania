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
from django.contrib.auth.models import User


def populate():

    data = {
        "name": "Wrestlemania 34",
        "date": "2018-04-08 19:00",
        "matches": {
            "universal_championship": {
                "wrestlers": ["Brock Lesnar", "Roman Reigns"],
                "match_type": Match.SINGLE
            },
            "wwe_championship": {
                "wrestlers": ["AJ Styles", "Shinsuke Nakamura"],
                "match_type": Match.SINGLE
            },
            "tag_match": {
                "wrestlers": ["Ronda Rousey", "Kurt Angle", "Stephanie McMahon", "Triple H"],
                "teams": {"Ronda Rousey & Kurt Angle": ["Ronda Rousey", "Kurt Angle"], 
                          "Stephanie McMahon & Triple H": ["Stephanie McMahon", "Triple H"]
                         },
                "match_type": Match.TAG
            },
            "tag_match2": {
                "wrestlers": ["Shane McMahon", "Daniel Bryan", "Kevin Owens", "Sami Zayn"],
                "teams": {"Shane McMahon & Daniel Bryan": ["Shane McMahon", "Daniel Bryan"], 
                          "Kevin Owens & Sami Zayn": ["Kevin Owens", "Sami Zayn"]
                         },
                "match_type": Match.TAG
            },
            "smackdown_womens_championship": {
                "wrestlers": ["Charlotte Flair", "Asuka"],
                "match_type": Match.SINGLE
            },
            "raw_womens_championship": {
                "wrestlers": ["Alexa Bliss", "Nia Jax"],
                "match_type": Match.SINGLE
            },
            "intercontinental_championship": {
                "wrestlers": ["The Miz", "Seth Rollins", "Finn Balor"],
                "match_type": Match.TRIPLE
            },
            "united_states_championship": {
                "wrestlers": ["Randy Orton", "Bobby Roode", "Jinder Mahal", "Rusev"],
                "match_type": Match.FOUR
            },
            "smackdown_tagteam_championship": {
                "wrestlers": ["Jey Uso", "Jimmy Uso", "Big E", "Kofi Kingston", "Xavier Woods", "Luke Harper", "Eric Rowan"],
                "teams": {"The Usos": ["Jey Uso", "Jimmy Uso"], 
                          "The New Day": ["Big E", "Kofi Kingston", "Xavier Woods"],
                          "The Bludgeon Brothers": ["Luke Harper", "Eric Rowan"]
                          },
                "match_type": Match.TRIPLE_TAG
            },
            "raw_tagteam_championship": {
                "wrestlers": ["Cesaro", "Sheamus", "Braun Strowman"],
                "teams": {"The Bar": ["Cesaro", "Sheamus"], 
                          "Braun Strowman & TBD": ["Braun Strowman",]
                          },
                "match_type": Match.TAG
            },
            "cruiserweight_championship": {
                "wrestlers": ["Cedric Alexander", "Mustafa Ali"],
                "match_type": Match.SINGLE
            },
            "taker_cena": {
                "wrestlers": ["Undertaker", "John Cena"],
                "match_type": Match.SINGLE
            },
            "womens_battle_royal": {
                "wrestlers": ["Bayley", "Sasha Banks","Ruby Riott","Sarah Logan","Liv Morgan","Becky Lynch","Naomi","Natalya","Lana","Mickie James","Mandy Rose","Sonya Deville","Carmella"], 
                "match_type": Match.ROYALE,
                "name": "WrestleMania Women's Battle Royal"
            },
            "andre_the_giant_battle_royal": {
                "wrestlers": ["Dolph Ziggler","Tyler Breeze","Fandango","Woken Matt Hardy","Baron Corbin",
                            "Mojo Rawley","Tye Dillinger","Dash Wilder","Scott Dawson","Goldust","Heath Slater",
                            "Rhyno","Zack Ryder","Primo Colon"],
                "match_type": Match.ROYALE,
                "name": "Andre the Giant Battle Royal"
            }
        },

        "users": {
            "deek": {
                "password": "password",
                "email": "deek@test.com",
                "first_name": "Derek",
                "last_name": "Russell"
            },
            "rusty": {
                "password": "password",
                "email": "rusty@test.com",
                "first_name": "Graeme",
                "last_name": "Russell"
            },
            "gordon": {
                "password": "password",
                "email": "gordon@test.com",
                "first_name": "Gordon",
                "last_name": "Daffurn"
            },
            "malky": {
                "password":"password",
                "email": "malky@test.com",
                "first_name": "Malcolm",
                "last_name": "Macvicar"
            },
            "innes": {
                "password": "password",
                "email": "innes@test.com",
                "first_name": "Murray",
                "last_name": "Innes"
            },
            "iain": {
                "password": "password",
                "email": "iain@test.com",
                "first_name": "Iain",
                "last_name": "Jack"
            },
            "lyle": {
                "password": "password",
                "email": "lyle@test.com",
                "first_name": "Lyle",
                "last_name": "Simpson"
            }
        }
    }

    # Test variables for comparing against the number of database results for each model after the populate script has run
    MATCH_COUNT = len(data["matches"])
    USER_COUNT = len(data["users"])
    WRESTLER_COUNT = 0
    TEAM_COUNT = 0
    for keys in data["matches"].values():
        WRESTLER_COUNT += len(keys["wrestlers"])
        if 'teams' in keys:
            TEAM_COUNT += len(keys["teams"])

    # Create event:
    wm34 = insert_event(data["name"], data["date"])
    
    # Create and link the other model entities
    for match_name, match_data in data["matches"].items():
        if Match.objects.count() < MATCH_COUNT:
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
    
    # Add users
    for username, user in data["users"].items():
        u = add_user(username, user["password"], user["email"], user["first_name"], user["last_name"])
    # Basic test that checks the correct number of entities have been entered to the DB
    test(MATCH_COUNT, WRESTLER_COUNT, TEAM_COUNT, USER_COUNT)       


# Database insert functions
def insert_event(name, date):
    e = Event.objects.get_or_create(name=name, date=date)[0]
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

def add_user(username,password,email,first_name,last_name):
    u = User.objects.get_or_create(username=username)[0]
    u.set_password(password)
    u.email = email
    u.first_name = first_name
    u.last_name = last_name
    if u.username in ["gordon", "lyle"]:
        u.is_staff = True
        u.is_superuser = True
    u.save()
    return u

def test(match_count, wrestler_count, team_count, user_count):
    m = Match.objects.count() == match_count
    w = Wrestler.objects.count() == wrestler_count
    t = Team.objects.count() == team_count
    u = User.objects.count() == user_count

    if m and w and t:
        print("Data entered successfully to the database")
    else:
        print("Something went wrong!")

if __name__ == '__main__':
    populate()