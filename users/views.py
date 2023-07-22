from django.shortcuts import render,get_object_or_404,redirect
import random
import uuid
from django.contrib.auth import get_user_model
User = get_user_model()
from django.http import HttpResponse,Http404
from django.core.cache import cache
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from email.message import EmailMessage
import smtplib
from secrets import compare_digest
#import mailtrap as mt
from .forms import RegisterFrom,createUserForm,UserLoginForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout

def send_mail(email_r, code_r):
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_HOST_USER = 'nimadfm1400@gmail.com'
    EMAIL_PORT_SSL = 465
    EMAIL_HOST_PASSWORD = 'eillarjyqtqczbsl'

    msg = EmailMessage()
    msg['Subject'] = 'verify'
    msg['From'] = EMAIL_HOST_USER
    msg['To'] = email_r
    msg.set_content(str(code_r))
    with smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT_SSL) as server:
        server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
        server.send_message(msg)

#برای رجیستر کردن ابتدا وارد این صفحه میشود و با زدن دکمه تایید برای او کد ارسال میشود و به تابع پایینی منتقل میشود
@csrf_exempt
@require_http_methods(["POST","GET"])
def register_v(request):
    if request.method == 'POST':
        form = RegisterFrom(request.POST)
        if form.is_valid():
        #phonemail = request.POST.get("phonemail")
            phonemail = form.cleaned_data['phonemail'] 
            code_random = random.randint(10000,99999)
            print(code_random)
            print(phonemail)
            try:
                #در این قسمت هم باید بر اساس شماره تلفن و هم بر اساس ایمیل چک شود
                print(code_random)
                if phonemail.isdigit():
                    user = User.objects.get(phone_number=phonemail)
                else:
                    user = User.objects.get(email=phonemail)
                print(code_random)
                return HttpResponse({'titl1': 'The code send to your phone. Please enter it.'})
            except User.DoesNotExist:
                if phonemail.isdigit():
                    cache.set(str(phonemail),str(code_random),3*60)
                    #send sms
                    response = redirect('/users/create/')
                    return response
                    #return HttpResponse({'title2': 'sms sabt'})
                else:
                    cache.set(str(phonemail),str(code_random),3*60)
                    send_mail(phonemail,code_random)
                    response = redirect('/users/create/')
                    return response
                    #return HttpResponse({'title3': 'email sabt'})
    else:
        form = RegisterFrom()
        
    return render(request,"users/register.html",{"form": form})
    #return HttpResponse({'title': 'The code send to your phone. Please enter it.'})

@csrf_exempt
@require_http_methods(["POST","GET"])
def create_user_v(request):
    print("1234")
    if request.method == 'POST':
        print("12345")
        form = createUserForm(request.POST)
        print("123123123")
        if form.is_valid():
            print("123123123")
            phonemail = form.cleaned_data['phonemail']
            code_rand = form.cleaned_data['code']
            password = form.cleaned_data['password']
            print(phonemail)
            print(code_rand)
            print(password)
            if phonemail.isdigit():
                code_cache = cache.get(str(phonemail))
                print(code_cache)
                print(code_rand)
                if not compare_digest(code_cache, code_rand):
                    return HttpResponse({'title1':'The entered code is invalid'})
                print("123123123")
                User.objects.create_user(phone_number=phonemail,password=password,username=phonemail)
                print("123123123")
                messages.success(request,'user registered successfully','success')
                response = redirect('/')
                return response            
                #return HttpResponse({'title9':'The entered code is invalid'})
            else:
                code_cache = cache.get(str(phonemail))
                print(code_cache)
                print(code_rand)
                print(type(code_cache))
                print(type(code_rand))
                if not compare_digest(code_cache,code_rand):
                    return HttpResponse({'title2':'The entered code is invalid'})
                print("120230")
                User.objects.create_user(email=phonemail,password=password,username=phonemail)
                messages.success(request,'user registered successfully','success')
                response = redirect('/')
                return response
                #return HttpResponse({'title8':'The entered code is invalid'})
    else:
        form = createUserForm()
    return render(request,"users/create_user.html",{"form": form})    
    #return HttpResponse({'title3':'Your information has been successfully registered'})     
            
            
@csrf_exempt
@require_http_methods(["POST","GET"])      
def login_v(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        print("123123123")
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,username=cd['phonemail'],password=cd['password'])
            if user is not None:
                login(request,user)
                messages.success(request,'logged successfully','success')
                return redirect('/')
            else:
                print("120")
                messages.error(request,'logged failed','failed')
                return redirect('/')    
                
    else:
        form = UserLoginForm()
            
    return render(request,"users/login.html",{"form": form})
  
          
def logout_v(request):
    logout(request)
    messages.success(request,'logged out successfully')
    return redirect('/')
             
        