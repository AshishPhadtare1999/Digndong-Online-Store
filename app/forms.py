from django import forms
from .models import Customer
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm, UsernameField,PasswordChangeForm
from django.forms import fields, models, widgets
from django.contrib.auth.models import User
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth import password_validation

class CustomerRegistrationForm(UserCreationForm):
    password1=forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2=forms.CharField(label='Confirm Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    email=forms.CharField(required=True,widget=forms.EmailInput(attrs={'class':'form-control'}))
    class Meta:
        model=User
        fields=['username','email','password1','password2']
        labels={'email':'Email'}
        widgets={'username':forms.TextInput(attrs={'class':'form-control'})}
    
class CustomerLoginForm(AuthenticationForm):
    username=UsernameField(widget=forms.TextInput(attrs={'class':'form-control','autofocus':True}))
    password=fields.CharField(label=_('Password'),strip=False,widget=forms.PasswordInput(attrs={'class':'form-control',
    'autocomplete':'current-password'}))

class CustomerChangePassword(PasswordChangeForm):
    old_password=forms.CharField(label=_('Old Password'),strip=False,
    widget=forms.PasswordInput(attrs={'class':'form-control','autocomplete':'current-password','autofocus':True}))
    new_password1=forms.CharField(label=_('New Password'),strip=False,
    widget=forms.PasswordInput(attrs={'class':'form-control','autocomplete':'new-password','autofocus':True}),
    help_text=password_validation.password_validators_help_text_html())
    new_password2=forms.CharField(label=_('Confirm Password'),strip=False,
    widget=forms.PasswordInput(attrs={'class':'form-control','autocomplete':'new-password','autofocus':True}))

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model=Customer
        fields=['name','locality','city','state','zipcode']
        widgets={'name':forms.TextInput(attrs={'class':'form-control'}),
        'locality':forms.TextInput(attrs={'class':'form-control'}),
        'city':forms.TextInput(attrs={'class':'form-control'}),
        'state':forms.Select(attrs={'class':'form-control'}),
        'zipcode':forms.NumberInput(attrs={'class':'form-control'}),
        
        }
