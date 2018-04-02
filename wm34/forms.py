from django import forms
from django.contrib.auth.models import User
from wm34.models import UserProfile
#from wm34.models import 

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