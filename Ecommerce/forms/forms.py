from django import forms


from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    #in form
    username =  forms.CharField(max_length=30, required=True, help_text='Required.')
    first_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')


    class Meta:
        #user is used as a model
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

# class LoginForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ("username", "password")
#         labels = {
#             'username' : 'Username',
#             'password' : 'Password'
#         }


# from django import forms
# from django.contrib.auth.models import User

# class LoginForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ("username", "password")
#         labels = {
#             'username' : 'Username',
#             'password' : 'Password'
#         }


# class SignupForm(forms.ModelForm):
#     password = forms.CharField(min_length=5, widget = forms.PasswordInput)
#     username =  forms.CharField(max_length=30, required=True, help_text='Required.')
#     first_name = forms.CharField(max_length=30, required=False, help_text='Required.')
#     last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
#     email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
#     class Meta:
#         model = User
#         fields = ("username","first_name", "last_name", "email", "password")
#         labels = {
#             'first_name': 'First Name',
#             'last_name' :'Last name',
#             'email' : 'Email'
#         }