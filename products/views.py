from django.shortcuts import render
from .models import Category , Product, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse



def ProductionList(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            posts = Product.objects.all()
            p = Paginator(posts,per_page=3)
            context = {'posts':p.object_list}
            return render(request,'products/ProductionList.html',context=context)
        else:
            return HttpResponse({"nima":"noooooo"})



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

def HomePage(request):
    return render(request,'homepage.html')