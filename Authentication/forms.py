from django import forms
from captcha.fields import CaptchaField

class RegisterFrom(forms.Form):
    phonemail = forms.CharField()
    
class createUserForm(forms.Form):
    phonemail = forms.CharField()
    code = forms.CharField()
    password = forms.CharField()
    captcha = CaptchaField()
    
class UserLoginForm(forms.Form):
    phonemail = forms.CharField()
    password = forms.CharField() 