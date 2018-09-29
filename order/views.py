from django.db.models import F
from django.http import HttpResponse
from django.shortcuts import render, redirect
import jsonpickle
from cart.models import CartItem
from utils.alipay import AliPay
import uuid
from order.models import *
from datetime import datetime


def index(request):
    user = request.session.get('user', '')
    cartitems = request.GET.get('cartitems', '')
    if user:
        return redirect('/order/orderlist?cartitems='+cartitems)
        # return render(request, 'order.html')
    return render(request, 'login.html', {'cartitems': cartitems, 'redirect':'order'})


def orderlist(request):
    cartitems = request.GET.get('cartitems', '')

    result = jsonpickle.loads('[' + cartitems+ ']')

    try:
        goods = [CartItem.objects.get(goods_id=i['goodsid'], color_id=i['colorid'], size_id=i['sizeid'], user=request.session['user']) for i in result]

    except Exception as e:
        pass
    return render(request, 'order.html', {'goodss':goods})


alipay = AliPay(appid='2016092100565827',
                app_notify_url='http://127.0.0.1:8000/order/checkpay/',
                app_private_key_path='order/keys/self_privite_key.txt',
                alipay_public_key_path='order/keys/alipay_public_key.txt',
                return_url='http://127.0.0.1:8000/order/checkpay/',
                debug=True)

def toorder(request):
    payway = request.GET.get('payway')
    address_id = request.GET.get('address')
    cartitems = request.GET.get('cartitems')
    totle_rmb = 0

    if payway == 'alipay':
        cartitems = jsonpickle.loads(cartitems)
        cartitem = [CartItem.objects.get(color_id=i['colorid'], goods_id=i['goodsid'], size_id=i['sizeid'], count=int(i['count']), user=request.session.get('user', ''), isdelete=False) for i in cartitems if i]
        for i in cartitem:
            totle_rmb += i.goods.price * i.count

        out_trade_num = uuid.uuid4().hex

        params = alipay.direct_pay(subject='电商支付', out_trade_no=out_trade_num, total_amount=str(totle_rmb))

        url = alipay.gateway + "?" + params

        user = request.session.get('user', '')

        order = Order.objects.create(order_num=datetime.now().strftime('%Y%m%d%H%M%S'), out_trade_num=out_trade_num, status='未支付', pay_way=payway, address=Address.objects.get(id=address_id,user=user), user=user)
        [OrderItem.objects.create(color_id=i['colorid'], goods_id=i['goodsid'], size_id=i['sizeid'], count=int(i['count']), order=order) for i in cartitems if i]

        return redirect(url)


def checkpay(request):
    params = request.GET.dict()
    sign = params.pop('sign')

    #进行校验是否支付成功
    if alipay.verify(params,sign):
        out_trade_num = params.get('out_trade_num')
        trade_no = params.get('trade_no')
        order = Order.objects.get(out_trade_num=out_trade_num)
        order.status = '待收货'
        order.trade_no = trade_no
        order.save()
        [ Inventory.objects.filter(goods=i.goods, size=i.size, color=i.color).update(count=F('count')-int(i.count)) for i in order.orderitem_set.all() if i]
        [ CartItem.objects.filter(goods=i.goods, size=i.size, color=i.color, count=i.count, user=request.session.get('user')).update(isdelete=True) for i in order.orderitem_set.all() if i]
        return HttpResponse('支付成功！')

    return HttpResponse('支付失败！')