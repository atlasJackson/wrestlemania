from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from django.contrib.auth.decorators import login_required

from wm34.models import User, Event, Match
from wm34.forms import UserForm, UserProfileForm, UserMatchAnswersForm

def index(request):
    events = Event.objects.order_by('event_slug')[:10]
    context_dict = {'events': events}
    return render(request,'wm34/index.html', context=context_dict)


def about(request):
    context_dict = {}
    return render(request, 'wm34/about.html', context=context_dict)


###############################################
# User-centric Views
###############################################

def sign_up(request):
    # A boolean value for telling the template
    # whether the registration was succesful.
    # Set to False initially. Code changes value to
    # True when registration succeeds.
    registered = False

    # If it's an HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        user_form = UserForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid():
            # Save the user's data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Update our variables to indicate that the template
            # registration was successful.
            registered = True
        else:
            # Print problems to the terminal.
            print(user_form.errors)
    else:
        # Not an HTTP POST, so we render our form using two ModelForm instances.
        # These forms will be blank, ready for user input.
        user_form = UserForm()

    # Render the template depending on the context.
    return render(request, 'wm34/sign_up.html', {'user_form': user_form, 'registered': registered})

def user_login(request):
    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        # We use request.POST.get('<variable>') as opposed
        # to request.POST['<variable>'] because the
        # request.POST.get('<variable>') returns None if the
        # value does not exist, while request.POST['<variable>']
        # will raise a KeyError exception.
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print("Invalid login details: {0}, {1}".format(username, password))
            return render(request, 'wm34/login.html', {"message": "Invalid login details. Please try again."})

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'wm34/login.html', {})

@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    return HttpResponseRedirect(reverse('index'))


###############################################
# Sort following into sections
###############################################

def show_event(request, event):

    try:
        # Get event with given slug.
        event = getEvent(event)
        matches = getMatches(event)
        context_dict = {'event': event, 'matches': matches}

    except Event.DoesNotExist:
        context_dict = {'event': None, 'matches': None}
        
    return render(request, 'wm34/show_event.html', context=context_dict)


@login_required
def event_scorecard(request, event):

    scorecard = UserMatchAnswersForm()

    try:
        # Get event with given slug.
        event = getEvent(event)
        matches = getMatches(event)
        context_dict = {'event': event, 'matches': matches}

    except Event.DoesNotExist:
        context_dict = {'event': None, 'matches': None}

    # An HTTP POST?
    if request.method == 'POST':
        scorecard = UserMatchAnswersForm(request.POST)

        # Have we been provided with a valid form?
        if scorecard.is_valid():
            # Save, but don't commit
            match_answers = scorecard.save(commit=False)

            # Get user entry from current user
            match_answers.user = request.user

            # Save the new UserMatchAnswers to the database
            scorecard.save()

            # Direct the user to the relevant event page.
            return HttpResponseRedirect(reverse('show_event', kwargs={'event':event}))

        else:
            # The supplied form contained errors - print them to the terminal.
            print(scorecard.errors)

    context_dict['scorecard'] = scorecard
    return render(request, 'wm34/event_scorecard.html', context=context_dict)


###############################################
# Helper functions
###############################################

# Get event with the given slug.
def getEvent(event_slug):
    return Event.objects.get(event_slug=event_slug)

# Get a list of all matches associated with the given event.
def getMatches(event):
    return [m for m in Match.objects.filter(event=event)]