from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput)
    
class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=30, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)
    
class DigitalWillForm(forms.Form):
    recipient = forms.CharField()
    amount = forms.FloatField()
    password = forms.CharField(widget=forms.PasswordInput)