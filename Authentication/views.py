#Django
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, Http404
from django.core.cache import cache
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model

#python
import random
import re
import smtplib
from secrets import compare_digest
from email.message import EmailMessage

#Local
from dj_laser.local_settings import GHASEDAK_CODE, LINE_NUMBER, HOST, HOST_PASSWORD, HOST_USER, PORT_SSL
from .forms import RegisterFrom, createUserForm, UserLoginForm, SetCodeForm, SetPassFrom

#Third Party
import ghasedakpack


User = get_user_model()


def send_sms(phonenumber, massage):
    try:
        sms = ghasedakpack.Ghasedak(GHASEDAK_CODE)
        temp = sms.send(
            {'message': massage, 'receptor': "09115147898", 'linenumber': LINE_NUMBER})
    except Exception as e:
        return HttpResponse({"detail": f"ERROR: {e}"})
    return temp


def send_mail(email_r, code_r):
    EMAIL_HOST = HOST
    EMAIL_HOST_USER = HOST_USER
    EMAIL_PORT_SSL = PORT_SSL
    EMAIL_HOST_PASSWORD = HOST_PASSWORD
    try:
        msg = EmailMessage()
        msg['Subject'] = 'verify'
        msg['From'] = EMAIL_HOST_USER
        msg['To'] = email_r
        msg.set_content(str(code_r))
        with smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT_SSL) as server:
            server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
            server.send_message(msg)
        print(code_r)
    except Exception as e:
        return HttpResponse({"detail":f"ERROR: {e}"})


def check_email(email):

    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if (re.fullmatch(regex, email)):
        return True
    return False


def check_phone(phone):

    regex = r'^989\d{9}$'
    if (re.fullmatch(regex, phone)):
        return True
    return False


def create_user_phone(phonemail, password, request):
    try:
        new_user = User.objects.create_user(
            username=phonemail, phone_number=phonemail, password=password)
        return new_user
    except Exception as e:
        messages.error(request, f"Error: {e}", "failed")
        return redirect('/')


def create_user_email(email, password, request):
    try:
        new_user = User.objects.create_user(
            email=email, password=password, username=email)
        return new_user
    except Exception as e:
        messages.error(request, f"Error: {e}", "failed")
        return redirect('/')


def register_v(request):
    if request.method == 'POST':
        form = RegisterFrom(request.POST)
        if form.is_valid():
            # phonemail = request.POST.get("phonemail")
            phonemail = form.cleaned_data['phonemail']
            code_random = random.randint(10000, 99999)
            print(code_random)
            user = None
            try:
                if phonemail.isdigit():
                    user = User.objects.get(phone_number=phonemail)
                else:
                    user = User.objects.get(email=phonemail)

                messages.error(
                    request, 'this phone number is alredy registered')
                # It returns to this page again
                return redirect(request.META.get('HTTP_REFERER'))
            except User.DoesNotExist:
                if phonemail.isdigit():
                    if not check_phone(phonemail):
                        return HttpResponse({"detail": "The phone number is invalid"})
                    cache.set(str(phonemail), str(code_random), 3*60)
                    result = send_sms(phonemail, code_random)
                    print(result)
                    response = redirect('/auth/create/')
                    return response
                else:
                    if not check_email(phonemail):
                        return HttpResponse({"detail": "The email is invalid"})
                    cache.set(str(phonemail), str(code_random), 3*60)
                    send_mail(phonemail, code_random)
                    return redirect('/auth/create/')
        else:
            messages.error(
                    request, 'data is not valid', 'error')
            response = redirect('/auth/register/')
            return response
    else:
        form = RegisterFrom()

    return render(request, "users/register.html", {"form": form})


def create_user_v(request):
    if request.method == 'POST':
        form = createUserForm(request.POST)
        if form.is_valid():
            phonemail = form.cleaned_data['phonemail']
            code_rand = form.cleaned_data['code']
            password = form.cleaned_data['password']
            if phonemail.isdigit():
                code_cache = cache.get(str(phonemail))
                if not compare_digest(code_cache, code_rand):
                    return HttpResponse({'detail': 'Compare is Not Valid'})
                new_user = create_user_phone(phonemail, password, request)
                messages.success(
                    request, 'user registered successfully', 'success')
                response = redirect('/auth/login/')
                return response
            else:
                code_cache = cache.get(str(phonemail))
                if not compare_digest(code_cache, code_rand):
                    return HttpResponse({'title2': 'The entered code is invalid'})
                new_user = create_user_email(phonemail, password, request)
                messages.success(
                    request, 'user registered successfully', 'success')
                return redirect('/auth/login/')
    else:
        form = createUserForm()
        return render(request, "users/create_user.html", {"form": form})


def login_v(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request, username=cd['phonemail'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'logged successfully', 'success')
                return redirect('/')
            else:
                messages.error(request, 'logged failed', 'failed')
                return redirect('/auth/login/')
        else:
            messages.error(
                request, 'The input information is incorrect', 'failed')
            return redirect('/auth/login/')

    else:
        form = UserLoginForm()
        return render(request, "users/login.html", {"form": form})


def logout_v(request):
    logout(request)
    messages.success(request, 'logged out successfully')
    return redirect('/')


#These three functions are used to forget the password
#function 1
def ForgotPassword_v(request):
    if request.method == "GET":
        # In this section, a form that takes the number or email will be displayed
        form = RegisterFrom()
        return render(request, "users/forget1.html/", {'form': form})
    else:
        # In this section, a code is sent to this number or email
        form = RegisterFrom(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            phonemail = cd['phonemail']
            try:
                if phonemail.isdigit():
                    user = User.objects.get(phone_number=phonemail)
                else:
                    user = User.objects.get(email=phonemail)
            except User.DoesNotExist:
                messages.warning(request,'this phone number is not alredy registered')
                return redirect("forget-password")
            code_random = random.randint(10000, 99999)
            print(code_random)
            if phonemail.isdigit():
                cache.set(str(phonemail), str(code_random), 3*60)
                result = send_sms(phonemail, code_random)
                
            else:
                cache.set(str(phonemail), str(code_random), 3*60)
                send_mail(phonemail, code_random)
            
            messages.success(request,"The code has been sent to you")
            return redirect('set-code')
                
#function 2
def SetCode_v(request):
    if request.method == "GET":
        form = SetCodeForm()
        return render(request, "users/forget2.html/", {'form': form})

    else:
        form = SetCodeForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            phonemail = cd['phonemail']
            code_rand = cd['code']
            code_cache = cache.get(str(phonemail))
            if not compare_digest(code_cache, code_rand):
                return HttpResponse({'detail': 'The entered code is invalid'})
            
            return redirect("set-password")

#function 3
def SetPassword_v(request):
    if request.method == "GET":
        form = SetPassFrom()
        return render(request, "users/forget1.html/", {'form': form})

    else:
        form = SetPassFrom(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            phonemail = cd['phonemail']
            password1 = cd['password1']
            password2 = cd['password2']
            if not compare_digest(password1, password2):
                return HttpResponse({'detail': 'The entered code is invalid'})
            if phonemail.isdigit():
                user = User.objects.get(phone_number=phonemail)
            else:
                user = User.objects.get(email=phonemail)
            user.set_password(f"{password1}")
            user.save()
            return redirect("user-login")
