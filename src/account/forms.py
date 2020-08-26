from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm

from .models import User, UserProfile


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=60, help_text='REQUIRED. ADD A VALID EMAIL ID.')
    registration_no=forms.CharField(max_length=20,help_text='ENTER YOUR COLLEGE REGISTRATION NO.')
    class Meta:
        model = User
        fields = ('email',
                  'username',
                  'registration_no',
                  'password1',
                  'password2')

    def clean_email(self):
        email = self.cleaned_data['email'].lower().strip()
        if email.count('@')==1:
            address,domain=email.split('@')
            #print('here is it:', address, domain)
            if '.' not in domain:
                self.add_error('email', 'Please use a valid email address')
        else:
            self.add_error('email','Please use a valid email address')
        #print(email)
        return email

class AccountAuthenticationForm(forms.ModelForm):
    password=forms.CharField(label='Password',widget=forms.PasswordInput)

    class Meta:
        model=User
        fields=('username','password')

    def clean(self):
        if self.is_valid():
            username=self.cleaned_data['username']
            password=self.cleaned_data['password']
            if not authenticate(username=username,password=password):
                raise forms.ValidationError('INVALID LOGIN CREDENTIALS')

class AccountUpdateForm(forms.ModelForm):
    class Meta:
        model=User
        fields=('username',)

    def clean_username(self):
        if self.is_valid():
            username=self.cleaned_data['username']
            try:
                account=User.objects.exclude(pk=self.instance.pk).get(username=username)#Cheks if the account already exists
            except User.DoesNotExist:
                return username
            raise forms.ValidationError('Username {} is already in use'.format(username))

class UserProfileForm(forms.ModelForm):

    class Meta:
        model=UserProfile
        fields=('name','hall','veg')

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        fields=('name','hall')
