# Django
from django.urls import reverse
from django.http import HttpResponse, Http404
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth import get_user_model

# Python 
import logging
import random

# Third Party
from azbankgateways import bankfactories, models as bank_models, default_settings as settings

# Local
from .models import Order
from Cart.models import Cart
from products.models import Product

User = get_user_model()

def callback_gateway_view(request):
    tracking_code = request.GET.get(settings.TRACKING_CODE_QUERY_PARAM, None)
    if not tracking_code:
        print("این لینک معتبر نیست.")
        return 0

    try:
        bank_record = bank_models.Bank.objects.get(tracking_code=tracking_code)
    except bank_models.Bank.DoesNotExist:
        print("این لینک معتبر نیست.")
        return 0

    # In this section, we must perform the corresponding record or any other appropriate action through the data in the record bank.
    if bank_record.is_success:
        print("پرداخت با موفقیت انجام شد.")
        return 10

    print("پرداخت با شکست مواجه شده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت.")
    return 20


# When returning from the bank, it is transferred to this function
def Ok_Record(request):
    # البت بهتر است که وقتی سفارشی ثبت شد یک پیام یا ایمیل برای ادمین فرستاده شود
    # In this part, we got the information related to the creation of the object
    # we have access to them through 'products':products,'price':TotalPrice,'user':user
    if request.method == "GET":
        status = callback_gateway_view(request)
        context = None
        match status:
            case 0:
                print("0")
            case 10:
                print("10")
            case 20:
                print("20")
            case 30:
                print("30")
            case 31:
                print("31")
                
        if status == 0:
            # If the return link is not valid
            messages.error(request, "این لینک معتبر نیست.", "failed")
            context = {
                "status": "این لینک معتبر نیست."
            }
        # void
        elif status == 10:
            pass
            # یک آبجکت میسازیم و ذخیره میکنیم و به ادمین یک پیغام میدهیم
            # تعداد و کد محصول ها در متغیر پایینی است
            products = Cart.objects.filter(user=request.user).values()
            ProductCodes = []
            ProductCounts = []
            for x in products:
                ProductCodes.append(str(list(x.values())[1]))
                ProductCounts.append(str(list(x.values())[2]))
            ###############################################
            # قیمت نهایی محاسبه شود
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
            # اینم برای یوزر
            #phonemail = str(request.user)
            #tempuser = ''
            #if phonemail.isdigit():
            #    tempuser = User.objects.get(phone_number=int(phonemail))
            #else:
            #    tempuser = User.objects.get(email=phonemail)
            
            tempuser = User.objects.get(id = request.user.id)
            ##################################

            ortemp = Order.objects.create(ProductCodes=ProductCodes, ProductCounts=ProductCounts, Price=TotalPrice, user=tempuser, Address=tempuser.address,
                                          consumed_code=random.randint(10000, 99999), status_pay=10)
            # حالا تمام سفارشات مربوز به
            # cart
            # که مربوط به این کاربر میباشد باید حذف شود
            products = Cart.objects.filter(user=request.user).delete()

            # به ادمین یک پیام جهت سفارش جدید زده میشود در این قسمت
            # messages.success(request,"Your order has been successfully placed")
            context = {
                "status": "Payment was successful"
            }
        # pay
        elif status == 20:
            # به هر دلیلی که پرداخت انجام نشد به این قسمت می آید
            messages.error(
                request, "پرداخت با شکست مواجه شده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت.", "failed")
            context = {
                "status": "Payment failed"
            }
        # error
        elif status == 30:
            pass
        # cancel
        elif status == 31:
            pass
        # refunded
        return render(request, "order/final.html/", context=context)
    else:
        return redirect('/')
