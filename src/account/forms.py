from django import forms 
from django.contrib.auth import password_validation
from django.contrib.auth.forms import AuthenticationForm,UsernameField, PasswordChangeForm, SetPasswordForm


class LoginFormAuthentication(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'class':'form-control form-control-user','placeholder': '',"autofocus": True, "id":"exampleInputEmail", "aria-describedby":"emailHelp"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control form-control-user','placeholder': '', "type":"password", "id":"exampleInputPassword"}))

class PasswordChangeForm(PasswordChangeForm, SetPasswordForm):
    old_password = forms.CharField(label="",widget=forms.PasswordInput(attrs={'class':'form-control','placeholder': 'Existing password',"autocomplete": "current-password", "autofocus": True} ))
    new_password1 = forms.CharField(label="",widget=forms.PasswordInput(attrs={'class':'form-control','placeholder': 'New password',"autocomplete": "new-password"}))
    new_password2 = forms.CharField(label="",widget=forms.PasswordInput(attrs={'class':'form-control','placeholder': 'Confirm password',"autocomplete": "new-password"}))
