from allauth.account.forms import SignupForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from django import forms

from .models import CustomUser


class CustomSignupForm(SignupForm):
    full_name = forms.CharField(max_length=50, label='Full Name',
            widget=forms.TextInput(attrs={'placeholder': 'Full Name'}))

    field_order = ['full_name', 'email', 'password1']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['full_name'].widget.attrs.update({'autofocus': 'autofocus'})
        

        for fieldname in ['email']:
            self.fields[fieldname].help_text = "Your ualberta email"

        for fieldname in ['password1']:
            self.fields[fieldname].help_text = "Don't use your ualberta password"

       
    
class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('full_name', 'bio')