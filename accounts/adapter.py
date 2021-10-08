from allauth.account.adapter import DefaultAccountAdapter
from django import forms

class UserAccountAdapter(DefaultAccountAdapter):
    def clean_email(self, email):
        """
        Check if the email ends with ualberta.ca
        """
        acceptable_domains = ('ualberta.ca',)
        if email.endswith(acceptable_domains):
            return email
        else:
            raise forms.ValidationError('Please use your ualberta email address.')

    
    def save_user(self, request, user, form, commit=True):
        """
        This is called when saving user via allauth registration.
        We override this to set additional data on user object.
        
        Reference: https://stackoverflow.com/questions/17634533/saving-custom-user-model-with-django-allauth
        """
        user = super(UserAccountAdapter, self).save_user(request, user, form, commit=False)
        user.full_name = form.cleaned_data.get('full_name')
        user.save()