from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={"placeholder": "Username"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password"}))
    captcha = forms.CharField(max_length=10, widget=forms.TextInput(attrs={"placeholder": "Enter Captcha"}))
