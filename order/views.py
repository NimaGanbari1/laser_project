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
from Authentication.views import send_sms
from dj_laser.local_settings import SHOP_OWNER_NUMBER

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
    # However, it is better to send a message or email to the admin when the order is registered
    # In this part, we got the information related to the creation of the object
    # we have access to them through 'products':products,'price':TotalPrice,'user':user
    if request.method == "GET":
        status = callback_gateway_view(request)
        context = None
        match status:
            # void
            case 0:
                # If the return link is not valid
                messages.error(request, "این لینک معتبر نیست.", "failed")
                context = {
                    "status": "این لینک معتبر نیست."
                }   
                
            # pay
            case 10:
                # Part 1
                products = Cart.objects.filter(user=request.user).values()
                ProductCodes = []
                ProductCounts = []
                for x in products:
                    ProductCodes.append(str(list(x.values())[1]))
                    ProductCounts.append(str(list(x.values())[2]))
                    
                # Part 2
                # Calculate the final price
                user = str(request.user)
                TotalPrice = 0
                for x in products:
                    temp = Product.objects.get(uniqe_code=list(x.values())[1])
                    price = temp.price
                    price *= list(x.values())[2]
                    TotalPrice += price
                # Part 3
                tempuser = User.objects.get(id = request.user.id)
                # Part 4
                rand_code = random.randint(10000, 99999)
                ortemp = Order.objects.create(ProductCodes=ProductCodes, ProductCounts=ProductCounts, Price=TotalPrice, user=tempuser, Address=tempuser.address,
                                            consumed_code=rand_code, status_pay=10)
                
                # Part 5
                # All items in the user's shopping cart will be deleted
                products = Cart.objects.filter(user=request.user).delete()

                # Part 6
                # A message will be sent to the admin for a new order in this section
                sms = send_sms(f"{SHOP_OWNER_NUMBER}",f"Hey, new order consumed_code: {rand_code}")
                
                # messages.success(request,"Your order has been successfully placed")
                context = {
                    "status": "Payment was successful"
                }
                
            # error    
            case 20:
                print("20")
                # به هر دلیلی که پرداخت انجام نشد به این قسمت می آید
                messages.error(
                    request, "پرداخت با شکست مواجه شده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت.", "failed")
                context = {
                    "status": "Payment failed"
                }
                
            # cancel    
            case 30:
                print("30")
                
            # refunded
            case 31:
                pass
            
        return render(request, "order/final.html/", context=context)
            
    else:
        return redirect('/')
