# Django
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.urls import reverse

# Local
from .forms import FinalAddresForm
from .models import Cart
from products.models import Product
from .forms import EditCartForm
from products.models import Product

# Third Party
from azbankgateways import bankfactories, models as bank_models, default_settings as settings
from azbankgateways.exceptions import AZBankGatewaysException
import logging

User = get_user_model()


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
    # This section is for making changes to the shopping cart, which is currently having a problem
    elif request.method == 'POST':
        # In this section, a number of forms will be sent to the server, and the information of all of them must be saved
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


# In this section, after seeing the products and editing section,
# you will enter the purchase finalization page, after which you will enter the payment page
def Final_v(request):
    # When the user clicks the option to finalize the purchase
    if request.method == "GET":
        if request.user.is_authenticated:
            # Part 1
            products = Cart.objects.filter(user=request.user).values()

            # Part 2
            # In this section, a list of products, a list of the price of each product is formed
            TotalPrice = 0
            TotalProduct = []
            PricePerGood = []
            for x in products:
                TotalProduct.append(Product.objects.get(
                    uniqe_code=list(x.values())[1]))
                temp = Product.objects.get(uniqe_code=list(x.values())[1])
                price = temp.price
                price *= list(x.values())[2]
                PricePerGood.append(price)
                TotalPrice += price

            # Part 3
            tempuser = User.objects.get(id=request.user.id)
            TotalAddress = tempuser.address

            intaial_data = {
                'count': TotalAddress
            }
            form = FinalAddresForm(initial=intaial_data)

            # Part 4
            # Final price + contact address + list of all products + final price of each product
            context = {'price': TotalPrice, 'address': form, 'product': TotalProduct,
                       'PricePerGood': PricePerGood, 'products': products}
            return render(request, 'users/FinalInspectionOfGoods.html/', context=context)

        else:
            messages.error(request, "please login ,tryagain", "failed")
            return redirect('/users/final/')

    # This is for when the user clicks the payment option
    elif request.method == "POST":
        """ In this section, when the user clicks the payment option, he comes to this section,
            and because we get the address, our method will be of the post type,
            and in this section, our address must be saved again."""
        if request.user.is_authenticated:
            form = FinalAddresForm(request.POST)
            if form.is_valid():
                # Part 1
                # Save the user's address
                cd = form.cleaned_data
                user = User.objects.get(id=request.user.id)
                user.address = cd['Address']
                user.save()

                # Part 2
                # Calculate the final price
                products = Cart.objects.filter(user=request.user).values()
                TotalPrice = 0
                for x in products:
                    # TotalProduct.append(Product.objects.get(uniqe_code=list(x.values())[1]))
                    temp = Product.objects.get(uniqe_code=list(x.values())[1])
                    price = temp.price
                    price *= list(x.values())[2]
                    TotalPrice += price

                # Part 3
                # The work related to the banking portal is done

                amount = TotalPrice
                user_mobile_number = '+989115147898'
                factory = bankfactories.BankFactory()
                try:
                    # or factory.create(bank_models.BankType.BMI) or set identifier
                    bank = factory.auto_create()
                    bank.set_request(request)
                    bank.set_amount(amount)
                    bank.set_client_callback_url('/order/register/')
                    bank.set_mobile_number(user_mobile_number)
                    bank_record = bank.ready()
                    return bank.redirect_gateway()

                except AZBankGatewaysException as e:
                    logging.critical(e)
                    # TODO: redirect to failed page.
                    raise e

            else:
                messages.error(request, "please login ,tryagain", "failed")
                return redirect('/')
        else:
            messages.error(request, "please login ,tryagain", "failed")
            return redirect('/users/final/')
