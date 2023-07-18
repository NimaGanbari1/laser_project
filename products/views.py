from django.shortcuts import render
from .models import Category , Product, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger




def ProductionList(request):
    if request.method == "GET":
        posts = Product.objects.all()
        p = Paginator(posts,per_page=3)
        context = {'posts':p.object_list}
        return render(request,'products/ProductionList.html',context=context)



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