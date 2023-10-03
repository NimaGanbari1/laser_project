from django.shortcuts import render, redirect
from .models import Category, Product, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from .forms import CreateCartForm, CreateCommentForm
from django.contrib import messages
from django.contrib.auth import get_user_model
User = get_user_model()


def ProductSearch(request):
    if request.method == "GET":
        # The title describes the category
        title = request.GET.get('q')
        context = {}
        posts = None
        try:
            posts = Product.objects.filter(title__icontains=title)
        except Product.DoesNotExist:
            return render(request, 'products/ProductionList.html', context=context)
        context = {'posts': posts}
        return render(request, 'products/ProductionList.html', context=context)
    else:
        return HttpResponse({"detail": f"Error: You do not have permission to access this method {request.method}"})


def create_cart(code1, count1, user1):
    try:
        new_cart = Cart.objects.create(Code=code1, Count=count1, user=user1)
        return new_cart
    except Exception as e:
        messages.error(request, f"Error: {e}", "failed")
        return redirect('/')
# Returns details about a product


def ProductDetail(request, id):
    # In this section, product details are displayed
    if request.method == "GET":

        # part 1
        # In this section, the desired product can be found from the database
        post = None
        try:
            post = Product.objects.get(uniqe_code=id)
        except Product.DoesNotExist:
            return HttpResponse({'detail': 'Your desired product was not found'})

        # part 2
        # In this section, the form related to adding to the cart is generated
        intaial_data = {
            'uniqeCode': id,
            'user': request.user,
            'count': 1
        }
        form = CreateCartForm(initial=intaial_data)
        # part 3
        # part 4
        # In this section, comments related to the product can be found
        # In this section, the names of users who have left comments can be found
        ListOfComment = None
        ListOfUserCom = []
        try:
            ListOfComment = Comment.objects.filter(Product=post).values()
            for temp in ListOfComment:
                temp1 = User.objects.get(id=list(temp.values())[1])
                ListOfUserCom.append(temp1.get_full_name())
        except Comment.DoesNotExist:
            return HttpResponse({'dont have comment': 'not found'})
        except User.DoesNotExist:
            return HttpResponse({'dont have comment': 'not found'})

        # part 5
        # In this section, the form related to the production of comments is created
        intaial_data1 = {
            'Product': post
        }
        CommentForm = CreateCommentForm(initial=intaial_data1)
        # part 6
        context = {'post': post, 'form': form, 'comment': ListOfComment,
                   'comform': CommentForm, 'users': ListOfUserCom}
        return render(request, 'products/ProductDetail.html', context=context)
    # When the user wants to add the desired product to the shopping cart, he is redirected to this section
    else:
        if request.user.is_authenticated:
            form = CreateCartForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                phonemail = cd['user']
                user = None
                if phonemail.isdigit():
                    user = User.objects.get(phone_number=int(phonemail))
                else:
                    user = User.objects.get(email=phonemail)

                new_cart = create_cart(cd['uniqeCode'], cd['count'], user)
                messages.success(request, "Added to cart")
                return redirect('/')
            else:
                messages.error(request, 'data is not validsss', 'failed')
                return redirect('/')
        else:
            messages.error(request, 'logged failed', 'failed')
            return redirect('/')


def create_comment(user1, product1, text1, request):
    try:
        new_comment = Comment.objects.create(
            user=user1, Product=product1, text=text1)
        return new_comment
    except Exception as e:
        messages.error(request, f"Error: {e}", "failed")
        return redirect('/')


def SetComment(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            user = User.objects.get(id=request.user.id)
            form = CreateCommentForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                # In this section, it is checked whether the user has a name or not
                # If you don't have a name, you can't comment
                if not user.first_name:
                    messages.error(
                        request, "To post a comment, you must first register your name in your profile. ,tryagain", "failed")
                    return redirect(f'/products/indexdetail/{product.uniqe_code}/')
                new_commnet = create_comment(
                    request.user, cd['Product'], cd['text'], request)
                messages.success(
                    request, "Your comment has been registered successfully")
                return redirect(f'/products/indexdetail/{product.uniqe_code}/')
            else:
                messages.error(request, "is not valid ,tryagain", "failed")
                return redirect('/')
        else:
            messages.error(request, "First, log in to your account", "failed")
            return redirect('/users/register')


def TypeCategory(request, type):
    Products = None
    try:
        if type == None or type == "None":
            Products = Product.objects.filter(is_active=True)
        else:
            temp = Category.objects.get(title=type,is_enable=True)
            Products = Product.objects.filter(categories=temp.id,is_active=True)
    except Product.DoesNotExist as e:
        raise e
    except Category.DoesNotExist as e:
        raise e
    return Products


def HomePage(request):
    if request.method == "GET":
        try:
            # In this section, the information related to the category is received through query params through form and is searched and checked
            # If it is for the first time or if he chooses the category of all, it will automatically return the None
            types = request.GET.get('category')
            # Products that include the desired category are selected
            Production = TypeCategory(request, types)
            categories = Category.objects.all()
            context = {'categories': categories, 'posts': Production}
            return render(request, 'homepage.html', context=context)
        except Exception as e:
            return HttpResponse({"detail": f"Error: {e}"})
    else:
        return HttpResponse({"detail": f"Error: You do not have permission to access this method {request.method}"})
