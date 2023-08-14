from django.shortcuts import render,redirect
from .models import Category , Product, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from .forms import CreateCartForm,CreateCommentForm
from users.models import Cart
from django.contrib import messages
from django.contrib.auth import get_user_model
User = get_user_model()


#تمامی محصولات را برمیگرداند
def ProductionList(request):
    if request.method == "GET":
        #if request.user.is_authenticated:
        posts = Product.objects.all()
        p = Paginator(posts,per_page=3)
        context = {'posts':p.object_list}
        return render(request,'products/ProductionList.html',context=context)
    else:
        return HttpResponse({"nima":"noooooo"})

#تمامی محصولات مربوط به صفحه منظور بر میگرداند
def index(request,page):
    posts = Product.objects.all()
    #page = request.GET.get('page', 1)

    paginator = Paginator(posts, 3)
    try:
        users = paginator.page(page).object_list
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    return render(request, 'products/indexProduction.html', { 'users': users })


#جزئیات مربوط به یک محصول را برمیگرداند 
def ProductDetail(request,id):
    #وقتی جزئیات محصول رو زد
    if request.method == "GET":
        try:
            post = Product.objects.get(uniqe_code=id)
        except Product.DoesNotExist:
            return HttpResponse({'title':'not found'})
        
        intaial_data ={
        'uniqeCode': id,
        'user': request.user,
        'count': 1
        }
        form = CreateCartForm(initial=intaial_data)
        print(form['uniqeCode'])
        print(form['count'])
        print(form['user'])
        #در این قسمت کامنت های این محصول نمایش داده میشود
        ListOfComment = Comment.objects.filter(Product=post)
        intaial_data1 ={
        'Product': post
        }
        CommentForm = CreateCommentForm(initial=intaial_data1)
        context = {'post':post,'form':form,'comment':ListOfComment,'comform':CommentForm}
        return render(request,'products/ProductDetail.html',context=context)
    #زمانی که مخاطب دکمه سابمیت را زد در صفحه جزئیات محصولات به این قسمت هدایت میشود
    else:
        print("nima1")
        if request.user.is_authenticated:
            print("nima1")
            form = CreateCartForm(request.POST)
            print("nima1")
            print(form['uniqeCode'])
            print(form['count'])
            print(form['user'])
            if form.is_valid():
                print("nima1")
                cd = form.cleaned_data
                print("nima1")
                phonemail = cd['user']
                print("1111111111111111111111111111111")
                print(type(phonemail))
                if phonemail.isdigit():
                    user = User.objects.get(phone_number = int(phonemail))
                else:
                    user = User.objects.get(email = phonemail)
                print("nima1")
                print(user)
                print(type(user))
                new_cart = Cart.objects.create(Code=cd['uniqeCode'],Count=cd['count'],user=user)
                print("nima1")
                #new_cart.save()
                print("nima1")
                return redirect('/')
            else:
                messages.error(request,'data is not validsss','failed')
                return redirect('/')
        else:
            messages.error(request,'logged failed','failed')
            return redirect('/')
                
        
def SetComment(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            phonemail = str(request.user)
            print("1111111111111111111111111111111")
            print(type(phonemail))
            if phonemail.isdigit():
                user = User.objects.get(phone_number = int(phonemail))
            else:
                user = User.objects.get(email = phonemail)  
            form = CreateCommentForm(request.POST)
            print("1111111111111111111111111111111")
            if form.is_valid():
                print("1111111111111111111111111111111")
                cd = form.cleaned_data
                product = cd['Product']
                if not user.first_name:
                    messages.error(request,"To post a comment, you must first register your name in your profile. ,tryagain","failed")
                    return redirect(f'/products/indexdetail/{product.uniqe_code}/')
                print("1111111111111111111111111111111")
                Comment.objects.create(user=request.user,Product=product,text=cd['text'])
                messages.success(request,"Your comment has been registered successfully")
                return redirect(f'/products/indexdetail/{product.uniqe_code}/')
            else:
                messages.error(request,"is not valid ,tryagain","failed")
                print("111")
                return redirect('/')
        else:
                messages.error(request,"First, log in to your account","failed")
                print("222")
                return redirect('/users/register')
                

def HomePage(request):
    return render(request,'homepage.html')