from django import forms
from django.contrib.auth.forms import PasswordChangeForm 
from django.core import validators


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, required=True, help_text='Required.')
    password = forms.CharField(max_length=100, required=True, help_text='Required.')
    
    
class RegistrationForm(forms.Form):
    name = forms.CharField(max_length=1500, required=True, help_text='Required.')
    username = forms.CharField(max_length=70, required=True, help_text='Required.')
    email = forms.CharField(max_length=200, required=True, help_text='Required.')
    phoneno = forms.CharField(max_length=20, required=True, help_text='Required.')
    password1 = forms.CharField(max_length=200, required=True, help_text='Required.')
    password2 = forms.CharField(max_length=200, required=True, help_text='Required.')
    ref = forms.CharField(max_length=200, required=False)
    
    
class PaymentForm(forms.Form):
    amount = forms.IntegerField()
    
    
class PasswordForm(forms.Form):
    old_pass = forms.CharField(max_length=100)
    new_pass1 = forms.CharField(max_length=100)
    new_pass2 = forms.CharField(max_length=100)
    
    
class PinCreationForm(forms.Form):
    pin1 = forms.CharField(max_length=10)
    pin2 = forms.CharField(max_length=10)
    
    
class PinUpdateForm(forms.Form):
    password = forms.CharField(max_length=150)
    u_pin1 = forms.CharField(max_length=10)
    u_pin2 = forms.CharField(max_length=10)


class ElectricityForm(forms.Form):
    disco = forms.CharField(max_length=70, required=True, help_text='Required.')
    meter = forms.CharField(max_length=70, required=True, help_text='Required.')
    amount = forms.CharField(max_length=70, required=True, help_text='Required.')
    b_number = forms.CharField(max_length=70, required=True, help_text='Required.')
    pin = forms.CharField(max_length=20, required=True, help_text='Required.')
    