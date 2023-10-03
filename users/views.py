from .forms import FinalAddresForm, ProfileForm, SetPassFrom, SetCodeForm
from django.http import HttpResponse, Http404
from order.models import Order
from azbankgateways.exceptions import AZBankGatewaysException
from azbankgateways import bankfactories, models as bank_models, default_settings as settings
from django.urls import reverse
import logging
import ghasedakpack
import requests
from tkinter import messagebox
from products.models import Product
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404, redirect
import uuid
from django.contrib.auth import get_user_model
User = get_user_model()
from Cart.models import Cart


def go_to_gateway_view(request, money):
    # خواندن مبلغ از هر جایی که مد نظر است
    amount = money
    # تنظیم شماره موبایل کاربر از هر جایی که مد نظر است
    # user_mobile_number = '+989112221234'  # اختیاری

    factory = bankfactories.BankFactory()
    # or factory.create(bank_models.BankType.BMI) or set identifier
    bank = factory.auto_create()
    bank.set_request(request)
    bank.set_amount(amount)
    # یو آر ال بازگشت به نرم افزار برای ادامه فرآیند
    bank.set_client_callback_url('/callback-gateway')
    # bank.set_mobile_number(user_mobile_number)  # اختیاری

    # در صورت تمایل اتصال این رکورد به رکورد فاکتور یا هر چیزی که بعدا بتوانید ارتباط بین محصول یا خدمات را با این
    # پرداخت برقرار کنید.
    bank_record = bank.ready()

    # هدایت کاربر به درگاه بانک
    return bank.redirect_gateway()


# در این قسمت بعد از دیدن محصولات و بخش ادیت وارد صفحه نهایی کردن خرید میشود که بعد از این صفحه وارد صفحه پرداخت میشود
@csrf_exempt
@require_http_methods(["GET", "POST"])
def Final_v(request):
    # زمانی که کاربر گزینه نهایی کردن خرید را میزند
    if request.method == "GET":
        if request.user.is_authenticated:
            products = Cart.objects.filter(user=request.user).values()
            TotalPrice = 0
            TotalProduct = []
            PricePerGood = []
            # در این حلقه قیمت نهایی و
            for x in products:
                TotalProduct.append(Product.objects.get(
                    uniqe_code=list(x.values())[1]))
                temp = Product.objects.get(uniqe_code=list(x.values())[1])
                price = temp.price
                price *= list(x.values())[2]
                PricePerGood.append(price)
                TotalPrice += price
            # tempuser = User.objects.get()
            # این قسمت برای گرفتن آدرس کاربر میباشد
            # phonemail = str(request.user)
            # tempuser = ""
            # if phonemail.isdigit():
            #    tempuser = User.objects.get(phone_number = int(phonemail))
            # else:
            #    tempuser = User.objects.get(email = phonemail)

            tempuser = User.objects.get(id=request.user.id)
            TotalAddress = tempuser.address

            intaial_data = {
                'count': TotalAddress
            }
            form = FinalAddresForm(initial=intaial_data)

            # قیمت نهایی +آدرس  مخاطب + لیست تمام محصولات+ قیمت نهایی هر محصول
            context = {'price': TotalPrice, 'address': form, 'product': TotalProduct,
                       'PricePerGood': PricePerGood, 'products': products}
            return render(request, 'users/FinalInspectionOfGoods.html/', context=context)

        else:
            messages.error(request, "please login ,tryagain", "failed")
            return redirect('/users/final/')
    # این برای زمانی است که کاربر گزینه پرداخت را میزند
    elif request.method == "POST":
        # در این قسمت زمانی که کاربر گزینه پرداخت را میزند به این قسمت می آید و به خاطر اینکه آدرس را
        # میگیریم از دوباره
        # پس متد ما از نوع پست خواهد بود و در این قسمت باید آدرسمون از دوباره سیو شود
        if request.user.is_authenticated:
            ######################################################
            # آدرس کاربر ذخیره شود
            form = FinalAddresForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                # phonemail = str(request.user)
                # if phonemail.isdigit():
                #    user = User.objects.get(phone_number = int(phonemail))
                # else:
                #    user = User.objects.get(email = phonemail)
                user = User.objects.get(id=request.user.id)
                user.address = cd['Address']
                user.save()
                ###############################################
                # قیمت نهایی محاسبه شود
                products = Cart.objects.filter(user=request.user).values()
                user = str(request.user)
                TotalPrice = 0
                for x in products:
                    # TotalProduct.append(Product.objects.get(uniqe_code=list(x.values())[1]))
                    temp = Product.objects.get(uniqe_code=list(x.values())[1])
                    price = temp.price
                    price *= list(x.values())[2]
                    # PricePerGood.append(price)
                    TotalPrice += price
                    # tempuser = User.objects.get()
                ##########################################################
                # به درگاه بانکی منتقل میشود و کار های حسابرسی انجام مشود
                # حالا یا از طریق بانک یا از طریق خودمون به تابع
                # ok_Record
                # منتقل میشوددر اپ
                # order
                # در این قسمت اطلاعات مربوط به ثبت سفارش به تابع مورد نظر ارسال مشود
                # temp5 = go_to_gateway_view(request,TotalPrice)
                # خواندن مبلغ از هر جایی که مد نظر است
                amount = TotalPrice
                # تنظیم شماره موبایل کاربر از هر جایی که مد نظر است
                user_mobile_number = '+989115147898'  # اختیاری

                factory = bankfactories.BankFactory()
                # or factory.create(bank_models.BankType.BMI) or set identifier
                bank = factory.auto_create()
                bank.set_request(request)
                bank.set_amount(amount)
                # یو آر ال بازگشت به نرم افزار برای ادامه فرآیند
                bank.set_client_callback_url('/order/register/')
                bank.set_mobile_number(user_mobile_number)  # اختیاری

                # در صورت تمایل اتصال این رکورد به رکورد فاکتور یا هر چیزی که بعدا بتوانید ارتباط بین محصول یا خدمات را با این
                # پرداخت برقرار کنید.
                bank_record = bank.ready()

                # هدایت کاربر به درگاه بانک
                return bank.redirect_gateway()
                # context = {'products':products,'price':TotalPrice,'user':user}
                # request.session['products'] = products
                # request.session['price'] = TotalPrice
                # request.session['user'] = user
            else:
                messages.error(request, "please login ,tryagain", "failed")
                return redirect('/')
        else:
            messages.error(request, "please login ,tryagain", "failed")
            return redirect('/users/final/')


@csrf_exempt
@require_http_methods(["GET"])
def About_v(request):
    if request.method == "GET":
        Address = "استان گلستان - شهرستان علی آباد کتول - خیابان پاسداران - پاسداران 50 - قدس 5"
        PhoneNumber = "09115147898"
        Email = "nimadfm1400@gmail.com"
        Description = "توضیحاتی درباره این شرکت و محصولات و غیره"
        context = {"address": Address, "phone": PhoneNumber,
                   'email': Email, 'des': Description}
        return render(request, 'users/about.html', context=context)


@csrf_exempt
@require_http_methods(["GET", "POST"])
def Profile_v(request):
    if request.method == "GET":
        # زمانی است که کاربر بر روی گزینه پروفایل کلیک میکند و به این صفحه منتقل میشود
        if request.user.is_authenticated:
            ########################################################
            # کاربر رو دریافت میکنیم
            # phonemail = str(request.user)
            # tempuser = ""
            # if phonemail.isdigit():
            #    tempuser = User.objects.get(phone_number = int(phonemail))
            # else:
            #    tempuser = User.objects.get(email = phonemail)
            #########################################################
            tempuser = User.objects.get(id=request.user.id)
            # اطلاعات کاربر رو به صورت پیش فرض ست میکنیم
            intaial_data = {
                'first_name': tempuser.first_name,
                'last_name': tempuser.last_name,
                # 'avatar'        : tempuser.avatar,
                'address': tempuser.address
            }
            form = ProfileForm(initial=intaial_data)
            # -------------------------------------------------------#
            orders = Order.objects.filter(user=tempuser)
            codetemp = []
            counttemp = []
            for x in orders:
                codetemp.append(x.ProductCodes)
                counttemp.append(x.ProductCounts)
            listpro = []
            for y in codetemp:
                temp = []
                for x in y:
                    temp1 = Product.objects.get(uniqe_code=x)
                    temp.append(temp1.title)
                listpro.append(temp)
            context = {'form': form, 'order': orders,
                       'listpro': listpro, 'counttemp': counttemp}
            return render(request, 'users/profile.html', context=context)

        else:
            messages.error(request, "please login ,tryagain", "failed")
            return redirect('/users/login/')
    elif request.method == "POST":
        # برای زمانی است که کاربر اطلاعات پروفایل خود را ادیت کرده است
        if request.user.is_authenticated:
            ######################################################
            # آدرس کاربر ذخیره شود
            form = ProfileForm(request.POST, request.FILES)
            user = User.objects.get(id=request.user.id)
            if form.is_valid():
                cd = form.cleaned_data
                tempuser = User.objects.get(id=request.user.id)
                tempuser.first_name = cd['first_name']
                tempuser.last_name = cd['last_name']
                tempuser.avatar = cd['avatar']
                tempuser.address = cd['address']
                tempuser.save()
                # form.save()
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

    response = messagebox.askyesno("please no", "are you sure?")
    if response == 0:
        messages.success(request, "The operation was canceled")
        return redirect('/users/profile/')
    User.objects.get(id=request.user.id).delete()
    messages.success(
        request, "Your account information has been saved successfully")
    return redirect('/')


def ForgotPassword_v(request):
    if request.method == "GET":
        # در این قسمت یک فرم که شماره یا ایمیل را بگیرد نمایش داده میشود
        form = RegisterFrom()
        return render(request, "users/forget1.html/", {'form': form})
    else:
        # در این قسمت یک کد برای این شماره یا ایمیل فرستاده میشود
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
                return HttpResponse({'this phone number is not alredy registered': 'The code send to your phone. Please enter it.'})
            code_random = random.randint(10000, 99999)
            if phonemail.isdigit():
                cache.set(str(phonemail), str(code_random), 3*60)
                # send sms
                response = redirect('/users/setcode/')
                return response
                # return HttpResponse({'title2': 'sms sabt'})
            else:
                cache.set(str(phonemail), str(code_random), 3*60)
                send_mail(phonemail, code_random)
                response = redirect('/users/setcode/')
                return response


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
                return HttpResponse({'title2': 'The entered code is invalid'})
            return redirect("/users/setpass/")


def SetPassword_v(request):
    if request.method == "GET":
        form = SetPassFrom()
        return render(request, "users/forget1.html/", {'form': form})
        # در این قسمت یک فرم نمایش داده میشود که یک شماره یا ایمیل و دو تا پسورد میخواهد
        pass
    else:
        # در این قسمت پسورد ها را چک کرده که مثل هم باشند و این پسورد برای کاربر ذخیره شود و به صفحه لاگین ریدایرکت شود
        form = SetPassFrom(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            phonemail = cd['phonemail']
            password1 = cd['password1']
            password2 = cd['password2']
            if not compare_digest(password1, password2):
                return HttpResponse({'The passwords do not match': 'The entered code is invalid'})
            if phonemail.isdigit():
                user = User.objects.get(phone_number=phonemail)
            else:
                user = User.objects.get(email=phonemail)
            user.set_password(f"{password1}")
            user.save()
            return redirect("/users/login/")
