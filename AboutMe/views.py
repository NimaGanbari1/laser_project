from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
@require_http_methods(["GET"])
def About_v(request):
    if request.method == "GET":
        Address = "استان گلستان - شهرستان علی آباد کتول - خیابان پاسداران - پاسداران 50 - قدس 5"
        PhoneNumber = "09115147898"
        Email = "nimadfm1400@gmail.com"
        Description = "توضیحاتی درباره این شرکت و محصولات و غیره"
        context = {"address": Address, "phone": PhoneNumber,
                   'email': Email, 'des': Description}
        return render(request, 'users/about.html', context=context)

