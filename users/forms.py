from django import forms
from products.models import Product
from django.contrib.auth import get_user_model
User = get_user_model()

class RegisterFrom(forms.Form):
    phonemail = forms.CharField()

class createUserForm(forms.Form):
    phonemail = forms.CharField()
    code = forms.CharField()
    password = forms.CharField()
    
class UserLoginForm(forms.Form):
    phonemail = forms.CharField()
    password = forms.CharField() 

class SetCodeForm(forms.Form):
    phonemail = forms.CharField()
    code = forms.CharField() 

class EditCartForm(forms.Form):
    count = forms.IntegerField()
    code = forms.IntegerField()
    
class FinalAddresForm(forms.Form):
    Address = forms.CharField()
    
    
    
class ProfileForm(forms.Form):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    #email = forms.EmailField(required=False)
    #phone_number = forms.IntegerField(required=False)
    avatar = forms.ImageField(required=False)
    address = forms.CharField(required=False)
    class Meta:
        model = User
        fields = ["first_name", "last_name","avatar","address"]
        #fields = "__all__"
        

class SetPassFrom(forms.Form):
    phonemail = forms.CharField()
    password1 = forms.CharField()
    password2 = forms.CharField()  
     