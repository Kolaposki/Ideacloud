"""
    name='forms',
    project='ideacloud'
    date='3/1/2020',
    author='Oshodi Kolapo',
"""
import datetime
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django.conf import settings


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(max_length=30, required=True, help_text='Username is Case Sensitive')
    email = forms.EmailField(max_length=254, help_text='Required. Provide a valid email address.')
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    gender = forms.ChoiceField(choices=((0, 'Male'), (1, 'Female')), required=True)
    agree = forms.BooleanField(required=False, label="Checking this box means you agree with the registration terms")

    class Meta:
        model = User  # Model to be affected is the User Model
        fields = ['username', 'first_name', 'last_name', 'gender', 'email', 'password1',
                  'password2']  # fields to be shown on form in order

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['agree'].widget.attrs.update({'class': 'ml-2'})
        self.fields['username'].widget.attrs.update({'autofocus': 'False'})


# Adding models to update fields
class UserUpdateForm(forms.ModelForm):
    username = forms.CharField()
    email = forms.EmailField()
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']  # fields to be updated by user


# Adding models to update fields
class ProfileUpdateForm(forms.ModelForm):
    # bio = forms.Textarea(help_text='Biography')
    location = forms.CharField(required=False, max_length=30, help_text='Location')
    birth_date = forms.DateField(required=False, help_text='Your date of birth - YY/M/D', initial=datetime.date.today)
    image = forms.ImageField(help_text='Update profile pic')

    class Meta:
        model = Profile
        fields = ['bio', 'birth_date', 'location', 'age', 'image']  # fields to be updated by user
