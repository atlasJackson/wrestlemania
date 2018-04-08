from django import forms
from django.contrib.auth.models import User
from wm34.models import UserProfile, UserMatchAnswers
from wm34.models import Match, Wrestler

###############################################
### USER FORMS
###############################################

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture', )

class EditUserForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


###############################################
### USER MATCH FORMS
###############################################

# Form corresponding to the answers for specific match types (5 points)
def UserMatchForm(*args, match, field_list, **kwargs):
    class UserMatchForm(forms.ModelForm):
        
        class Meta:
            model=UserMatchAnswers
            fields = field_list

        def __init__(self, *args, **kwargs):
            super(UserMatchForm,self).__init__(*args, **kwargs)
            if match:
                # The fields for which we need to generate the choioces from competitors in the match.
                fields_with_wrestler_choices = ['winner', 'who_pins', 'who_pinned', 'first_out', 
                                                'final_four_one', 'final_four_two', 'final_four_three', 'final_four_four']
                # Populate choices of above fields if they're included.
                for field in field_list:
                    if field in fields_with_wrestler_choices:
                        get_competitors_for_field(self, match, field)

    return UserMatchForm()


###############################################
# Helper functions
###############################################

def get_competitors_for_field(this_form, match, field):
    # Specific check for field 'winner'.
    if field == 'winner':
        if match.team.all():
            this_form.fields[field] = forms.ChoiceField(
                choices=[(t.id, str(t)) for t in match.team.all()])
        else:
            this_form.fields[field] = forms.ChoiceField(
                choices=[ (w.id, str(w)) for w in match.wrestler.all()])

    # Every other field requires choices from a list of individual competitors.
    else:
        this_form.fields[field] = forms.ChoiceField(
                choices=[ (w.id, str(w)) for w in match.wrestler.all()])


