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
        return p.object_list
        #return render(request,'products/ProductionList.html',context=context)
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

def ProductSearch(request):
    if request.method == "GET":
        title = request.GET.get('q')
        context = {}
        posts = None
        try:
            posts = Product.objects.filter(title__icontains =title)
        except Product.DoesNotExist:
            return render(request,'products/ProductionList.html',context=context)
        p = Paginator(posts,per_page=3)
        context = {'posts':p.object_list}
        return render(request,'products/ProductionList.html',context=context)
        

#جزئیات مربوط به یک محصول را برمیگرداند 
def ProductDetail(request,id):
    #وقتی جزئیات محصول رو زد
    if request.method == "GET":
        post = None
        try:
            post = Product.objects.get(uniqe_code=id)
        except Product.DoesNotExist:
            return HttpResponse({'title':'not found'})
        #ditemp = list(list(post.categories.values())[0].values())[1]
        intaial_data ={
        'uniqeCode': id,
        'user': request.user,
        'count': 1
        }
        form = CreateCartForm(initial=intaial_data)
        #در این قسمت کامنت های این محصول نمایش داده میشود
        try:
            ListOfComment = Comment.objects.filter(Product=post).values()
        except Comment.DoesNotExist:
            return HttpResponse({'dont have comment':'not found'})
        ListOfUserCom = []
        try:
            for temp in ListOfComment:
                temp1 = User.objects.get(id=list(temp.values())[1])
                ListOfUserCom.append(temp1.get_full_name())
        except User.DoesNotExist:
            return HttpResponse({'dont have comment':'not found'})
            
        #در ادامه یک گزینه برای حذف کردن کامنت خود در بخش کامنت ها بگذاریم
        intaial_data1 ={
        'Product': post
        }
        CommentForm = CreateCommentForm(initial=intaial_data1)
        context = {'post':post,'form':form,'comment':ListOfComment,'comform':CommentForm,'users':ListOfUserCom}
        return render(request,'products/ProductDetail.html',context=context)
    #زمانی که مخاطب دکمه سابمیت را زد در صفحه جزئیات محصولات به این قسمت هدایت میشود
    else:
        if request.user.is_authenticated:
            form = CreateCartForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                phonemail = cd['user']
                if phonemail.isdigit():
                    user = User.objects.get(phone_number = int(phonemail))
                else:
                    user = User.objects.get(email = phonemail)
                    
                
                new_cart = Cart.objects.create(Code=cd['uniqeCode'],Count=cd['count'],user=user)
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
            #phonemail = str(request.user)
            #if phonemail.isdigit():
            #    user = User.objects.get(phone_number = int(phonemail))
            #else:
            #    user = User.objects.get(email = phonemail)  
                
            user = User.objects.get(id = request.user.id)
            form = CreateCommentForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                product = cd['Product']
                if not user.first_name:
                    messages.error(request,"To post a comment, you must first register your name in your profile. ,tryagain","failed")
                    return redirect(f'/products/indexdetail/{product.uniqe_code}/')
                Comment.objects.create(user=request.user,Product=product,text=cd['text'])
                messages.success(request,"Your comment has been registered successfully")
                return redirect(f'/products/indexdetail/{product.uniqe_code}/')
            else:
                messages.error(request,"is not valid ,tryagain","failed")
                return redirect('/')
        else:
                messages.error(request,"First, log in to your account","failed")
                return redirect('/users/register')

def TypeCategory(request,type):
    Products = None
    if type == None or type == "None":
        Products = Product.objects.all()
    else:
        temp = Category.objects.get(title=type)
        Products = Product.objects.filter(categories = temp.id)
    return Products            

def HomePage(request):
    type = request.GET.get('category')
    Production = TypeCategory(request,type)
    categories = Category.objects.all()
    #p = ProductionList(request)
    context = {'categories':categories,'posts':Production}
    return render(request,'homepage.html',context=context)