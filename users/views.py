# Django
from django.http import HttpResponse, Http404
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model

# Local
from products.models import Product
from Cart.models import Cart
from .forms import ProfileForm
from order.models import Order

# Python
import logging
import ghasedakpack
import requests
from tkinter import messagebox


User = get_user_model()


def Profile_v(request):
    # It is when the user clicks on the profile option and is transferred to this page
    if request.method == "GET":
        if request.user.is_authenticated:
            # part 1
            tempuser = User.objects.get(id=request.user.id)
            # part 2
            # We set the user information as default
            intaial_data = {
                'first_name': tempuser.first_name,
                'last_name': tempuser.last_name,
                'address': tempuser.address
            }
            form = ProfileForm(initial=intaial_data)
            # part 3
            # This section is used to display orders
            orders = Order.objects.filter(user=tempuser)
            codetemp = []
            # The number of each product ordered
            counttemp = []
            for x in orders:
                codetemp.append(x.ProductCodes)
                counttemp.append(x.ProductCounts)
            # List of ordered products
            listpro = []
            for y in codetemp:
                temp = []
                for x in y:
                    temp1 = Product.objects.get(uniqe_code=x)
                    temp.append(temp1.title)
                listpro.append(temp)
            # part 4
            context = {'form': form, 'order': orders,
                       'listpro': listpro, 'counttemp': counttemp}
            return render(request, 'users/profile.html', context=context)

        else:
            messages.error(request, "please login ,tryagain", "failed")
            return redirect('/auth/login/')

    elif request.method == "POST":
        # It is for when the user has edited his profile information
        if request.user.is_authenticated:
            form = ProfileForm(request.POST, request.FILES)
            if form.is_valid():
                cd = form.cleaned_data
                # Because we authenticated at the beginning, there is no need for Try
                user = User.objects.get(id=request.user.id)
                user.first_name = cd['first_name']
                user.last_name = cd['last_name']
                user.avatar = cd['avatar']
                user.address = cd['address']
                user.save()

                messages.success(
                    request, "Your account information has been saved successfully")
                return redirect('/users/profile/')
            else:
                messages.error(
                    request, "data is not valid ,tryagain", "failed")
                return redirect('/users/profile/')
        else:
            messages.error(request, "please login ,tryagain", "failed")
            return redirect('/users/profile/')


def delete_v(request):

    response = messagebox.askyesno("are you sure?", "")
    if response == 0:
        messages.success(request, "The operation was canceled")
        return redirect('/users/profile/')
    User.objects.get(id=request.user.id).delete()
    messages.success(
        request, "Your account has been successfully deleted")
    return redirect('/')
