# Django
from django.shortcuts import render

# Local
from .models import About


def About_v(request):
    if request.method == "GET":
        about = About.objects.get(code=1)
        Address = about.Address
        PhoneNumber = about.phoneNumber
        Email = about.email
        Description = about.description
        context = {"address": Address, "phone": PhoneNumber,
                   'email': Email, 'des': Description}
        return render(request, 'users/about.html', context=context)
