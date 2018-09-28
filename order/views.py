from django.shortcuts import render


def index(request):
    cartitems = request.GET.get('cartitems', '')
    print(cartitems)
    return render(request, 'order.html')


def toorder(request):
    return None