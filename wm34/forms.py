from django import forms
from django.contrib.auth.models import User
from wm34.models import UserProfile, UserMatchAnswers
from wm34.models import Match, Wrestler

###################################
### USER FORMS
###################################

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


# Form for handling match winner
class UserMatchWinnerForm(forms.ModelForm):

    class Meta:
        model=UserMatchAnswers
        fields = ('winner',)

    def __init__(self, *args, **kwargs):
        match = kwargs.pop('match', None)
        super(UserMatchWinnerForm,self).__init__(*args, **kwargs)
        if match:
            if match.team.all():
                self.fields['winner'] = forms.ChoiceField(
                    choices=[(t.id, str(t)) for t in match.team.all()])
            else:
                self.fields['winner'] = forms.ChoiceField(
                    choices=[ (w.id, str(w)) for w in match.wrestler.all()])


# Form corresponding to the answers for all match types (10 points)
def UserMatchBasicForm(include_list=[], *args, **kwargs):
    class MyUserMatchBasicForm(forms.ModelForm):
        
        class Meta:
            model=UserMatchAnswers
            fields = include_list

    return MyUserMatchBasicForm()

# Form corresponding to the answers for specific match types (5 points)
def UserMatchSpecificForm(include_list=[], *args, **kwargs):
    class MyUserMatchSpecificForm(forms.ModelForm):
        
        class Meta:
            model=UserMatchAnswers
            fields = include_list
        
    return MyUserMatchSpecificForm()
