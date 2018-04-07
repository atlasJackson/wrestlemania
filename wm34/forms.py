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


class UserMatchAnswersForm(forms.ModelForm):
    class Meta:
        model=UserMatchAnswers
        fields = ('winner',)

    def __init__(self, *args, **kwargs):
        match = kwargs.pop('match', None)
        super(UserMatchAnswersForm,self).__init__(*args, **kwargs)
        if match:
            self.fields['winner'] = forms.ChoiceField(
                choices=[ (w.id, str(w)) for w in match.wrestler.all()])