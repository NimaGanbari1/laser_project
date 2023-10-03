from dj_laser.local_settings import GHASEDAK_CODE, LINE_NUMBER, HOST, HOST_PASSWORD, HOST_USER, PORT_SSL
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, Http404
import re
import smtplib
from email.message import EmailMessage
from django.contrib import messages
from secrets import compare_digest
import ghasedakpack
from django.core.cache import cache
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .forms import RegisterFrom, createUserForm, UserLoginForm
import random
from django.contrib.auth import get_user_model
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

    msg = EmailMessage()
    msg['Subject'] = 'verify'
    msg['From'] = EMAIL_HOST_USER
    msg['To'] = email_r
    msg.set_content(str(code_r))
    with smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT_SSL) as server:
        server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
        server.send_message(msg)
    print(code_r)


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


@csrf_exempt
@require_http_methods(["POST", "GET"])
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
                # در این قسمت هم باید بر اساس شماره تلفن و هم بر اساس ایمیل چک شود
                if phonemail.isdigit():
                    user = User.objects.get(phone_number=phonemail)
                else:
                    user = User.objects.get(email=phonemail)
                # return HttpResponse({'detail': 'this phone number is alredy registered'})
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
        form = RegisterFrom()

    return render(request, "users/register.html", {"form": form})


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


@csrf_exempt
@require_http_methods(["POST", "GET"])
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


@csrf_exempt
@require_http_methods(["POST", "GET"])
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
