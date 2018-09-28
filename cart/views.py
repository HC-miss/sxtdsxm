from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from .models import CartItem
from goods.models import *


def index(request):
    if request.method == 'POST':
        colorid = request.POST.get('colorid', '')
        goodsid = request.POST.get('goodsid', '')
        sizeid = request.POST.get('sizeid', '')
        type = request.POST.get('type', '')

        count = request.POST.get('count', '')

        user = request.session.get('user', '')

        color = Color.objects.get(id=colorid)
        size = Size.objects.get(id=sizeid)
        goods = Goods.objects.get(id=goodsid)
        if user:
            cart = CartItem.objects.filter(goods=goods, color=color, size=size, user=user)
            if type == 'add':
                if cart:
                    cart[0].count = int(count) + int(cart[0].count)
                    cart[0].save()
                else:
                    CartItem.objects.create(goods=goods, color=color, size=size, count=count, user=user)
                    return render(request, 'cart.html')
            elif type == 'delete':
                if cart:
                    cart[0].isdelete = True
                    cart[0].save()
                    return JsonResponse({'flag': True})
                return JsonResponse({'flag': False})
            elif type == 'minus' :
                if cart:
                    cart[0].count -= 1
                    cart[0].save()
                    return JsonResponse({'flag': True})
                return JsonResponse({'flag': False})
            elif type == 'plus':
                if cart:
                    cart[0].count += 1
                    cart[0].save()
                    return JsonResponse({'flag': True})
                return JsonResponse({'flag': False})
        else:
            cart = request.session.get('cart', {})
            cart_name = goodsid + ',' + colorid + ',' + sizeid
            print(cart)
            if type == 'add':
                if cart_name in cart:
                    cart[cart_name][3] = int(count)
                else:
                    cart[cart_name] = [goods, color, size, int(count)]
                    request.session['cart'] = cart
                return redirect('/cart/')
            elif type == 'delete':
                if cart_name in cart:
                    del cart[cart_name]
                    request.session['cart'] = cart
                    return JsonResponse({'flag': True})
                return JsonResponse({'flag': False})
            elif type == 'minus':
                if cart_name in cart:
                    cart[cart_name][3] -= 1
                    request.session['cart'] = cart
                    return JsonResponse({'flag': True})
                return JsonResponse({'flag': False})
            elif type == 'plus':
                if cart_name in cart:
                    cart[cart_name][3] += 1
                    request.session['cart'] = cart
                    return JsonResponse({'flag': True})
                return JsonResponse({'flag': False})
    else:
        cart = request.session.get('cart', None)
        return render(request, 'cart.html', {'cart': cart})
