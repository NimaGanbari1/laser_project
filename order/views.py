from django.shortcuts import render,get_object_or_404,redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from users.models import Cart
from products.models import Product
from django.contrib.auth import get_user_model
User = get_user_model()
from .models import Order
import random
from django.contrib import messages
def ReqForCheck():
    return 10

@csrf_exempt
@require_http_methods(["GET","POST"])
def Ok_Record(request):
    #ابتدا به بانک درخواست میدهیم که این کاربر آیا پرداخت موفقی داشته است یا خیر؟
    #در صورتی که اوکی بود یک آبجکت ساخته میشود و سیو میشود
    #البت بهتر است که وقتی سفارشی ثبت شد یک پیام یا ایمیل برای ادمین فرستاده شود
    #ولی اگر اوکی نبود به کاربر نمایش داده شود که پرداخت با  مشکل مواجه شده است و از دوباره تلاش کند
    #در این قسمت ما اطلاعات مربوط به ساخت آبجکت را گرفتیم و با 
    #'products':products,'price':TotalPrice,'user':user
    #به آنها دسترسی داریم
    print(request.method)
    if request.method == "GET":
        print("10")
        #print(request.session.get('price'))
        #print(request.POST['price'])
        print("11")
        status = ReqForCheck()
        if status == 0:
            pass
        #void
        elif status == 10:
            pass
            #یک آبجکت میسازیم و ذخیره میکنیم و به ادمین یک پیغام میدهیم
            #تعداد و کد محصول ها در متغیر پایینی است
            products = Cart.objects.filter(user=request.user).values()
            ProductCodes = []
            ProductCounts = []
            for x in products:
                ProductCodes.append(str(list(x.values())[1]))
                ProductCounts.append(str(list(x.values())[2]))
            ###############################################
            #قیمت نهایی محاسبه شود
            print(products)
            print("nima7898")
            user = str(request.user)
            TotalPrice = 0
            for x in products:
                print(x)
                print("nima2")
                #TotalProduct.append(Product.objects.get(uniqe_code=list(x.values())[1]))
                print("nima3")
                temp = Product.objects.get(uniqe_code=list(x.values())[1])
                print("nima4")
                price = temp.price
                print("nima5")
                price *= list(x.values())[2]
                print("nima6")
                print(price)
                #PricePerGood.append(price)
                print("nima7")
                TotalPrice += price
                print("nima8")
                print(TotalPrice)
                #tempuser = User.objects.get()
            ##########################################################
            #اینم برای یوزر
            phonemail = str(request.user)
            print("nimaaa")
            print(phonemail)
            tempuser = ''
            if phonemail.isdigit():
                print("nimaaa")
                tempuser = User.objects.get(phone_number = int(phonemail))
            else:
                print("nimaaa22")
                tempuser = User.objects.get(email = phonemail)
            ##################################
            
            Order.objects.create(ProductCodes=ProductCodes,ProductCounts=ProductCounts,Price=TotalPrice,user=tempuser,Address=tempuser.address,
                                 consumed_code=random.randint(10000,99999),status_pay=10)
            #حالا تمام سفارشات مربوز به 
            #cart
            #که مربوط به این کاربر میباشد باید حذف شود
            products = Cart.objects.filter(user=request.user).delete()
            
            #به ادمین یک پیام جهت سفارش جدید زده میشود در این قسمت
            messages.success(request,"Your order has been successfully placed")
            return redirect('/')
        #pay
        elif status == 20:
            pass
        #error
        elif status == 30:
            pass
        #cancel
        elif status == 31:
            pass
        #refunded
        return redirect('/') 
    return redirect('/')
    
