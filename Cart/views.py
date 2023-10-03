from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .models import Cart
from products.models import Product
from .forms import EditCartForm


@csrf_exempt
@require_http_methods(["GET", "POST"])
def Cart_v(request):
    # When the user wants to see his shopping cart, he is transferred to this page
    if request.method == 'GET':
        if request.user.is_authenticated:
            # part 1
            # In this section, the list of stored cart is read from the database
            list_of_product = Cart.objects.filter(user=request.user).values()

            temp1 = ''
            if not list_of_product:
                temp1 = 'the list is empty'
            # part 2
            # part 3
            # In this section, the list of products stored in the user's shopping cart is read from the database
            # In this section, the number and code of ordered products are stored in forms
            products2 = []
            ListForm = []
            for x in list_of_product:
                temp = Product.objects.get(uniqe_code=list(x.values())[1])
                products2.append(temp)
                intaial_data = {
                    'count': list(x.values())[2],
                    'code': list(x.values())[1]
                }
                form = EditCartForm(initial=intaial_data)
                ListForm.append(form)
            # part 4
            # List of products based on object + list of forms + if the list is empty
            context = {'products2': products2,
                       'ListForm': ListForm, 'temp': temp1}
            return render(request, "users/cart.html", context=context)
        else:
            messages.error(request, "please login ,tryagain", "failed")
            return redirect('/')
    #This section is for making changes to the shopping cart, which is currently having a problem
    elif request.method == 'POST':
        #In this section, a number of forms will be sent to the server, and the information of all of them must be saved
        forms = EditCartForm(request.POST)
        if forms.is_valid():
            cd = forms.cleaned_data
            list_of_product = Cart.objects.filter(user=request.user).values()
            for x in list_of_product:
                for temp in cd:
                    if int(list(x.values())[1]) == int(temp['code']):
                        list(x.values())[2] = temp['count']
                        list(x.values())[2].save()
            messages.success(request, 'logged out successfully')
            return redirect('/users/cart/')
        else:
            messages.error(request, "please login ,tryagain", "failed")
            return redirect('/')
        return redirect('/users/cart/')


