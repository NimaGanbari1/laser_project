from azbankgateways import bankfactories, models as bank_models, default_settings as settings
from django.urls import reverse
from django.http import HttpResponse, Http404
import logging
from django.contrib import messages
import random
from .models import Order
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from users.models import Cart
from products.models import Product
from django.contrib.auth import get_user_model
User = get_user_model()

#در هنگام بازگشت از بانک به این تابع منتقل میشود
def callback_gateway_view(request):
    tracking_code = request.GET.get(settings.TRACKING_CODE_QUERY_PARAM, None)
    if not tracking_code:
        print("این لینک معتبر نیست.")
        return 0

    try:
        bank_record = bank_models.Bank.objects.get(tracking_code=tracking_code)
    except bank_models.Bank.DoesNotExist:
        print("این لینک معتبر نیست2.")
        return 0

    # در این قسمت باید از طریق داده هایی که در بانک رکورد وجود دارد، رکورد متناظر یا هر اقدام مقتضی دیگر را انجام دهیم
    if bank_record.is_success:
        # پرداخت با موفقیت انجام پذیرفته است و بانک تایید کرده است.
        # می توانید کاربر را به صفحه نتیجه هدایت کنید یا نتیجه را نمایش دهید.
        print("پرداخت با موفقیت انجام شد.")
        return 10

    # پرداخت موفق نبوده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت.
    print("پرداخت با شکست مواجه شده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت.")
    return 20


@csrf_exempt
@require_http_methods(["GET", "POST"])
def Ok_Record(request):
    # ابتدا به بانک درخواست میدهیم که این کاربر آیا پرداخت موفقی داشته است یا خیر؟ در تابع بالایی
    # در صورتی که اوکی بود یک آبجکت ساخته میشود و سیو میشود
    # البت بهتر است که وقتی سفارشی ثبت شد یک پیام یا ایمیل برای ادمین فرستاده شود
    # ولی اگر اوکی نبود به کاربر نمایش داده شود که پرداخت با  مشکل مواجه شده است و از دوباره تلاش کند
    # در این قسمت ما اطلاعات مربوط به ساخت آبجکت را گرفتیم و با
    # 'products':products,'price':TotalPrice,'user':user
    # به آنها دسترسی داریم
    if request.method == "GET":
        status = callback_gateway_view(request)
        context = None
        if status == 0:
            # اگر لینک بازگرداننده معتبر نباشد
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
