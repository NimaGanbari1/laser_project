# django
from django import forms
from django.contrib.auth import get_user_model


User = get_user_model()


class ProfileForm(forms.Form):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    avatar = forms.ImageField(required=False)
    address = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "avatar", "address"]
