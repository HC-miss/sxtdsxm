from io import BytesIO
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from PIL import Image, ImageDraw, ImageFont
import random
# from hashlib import md5
from cart.models import CartItem
from .models import UserInfo, Area, Address
# import jsonpickle
from django.core import serializers


def login(request):
    if request.method == 'POST':
        account = request.POST.get('account')
        password = request.POST.get('password')
        red = request.POST.get('redirect')
        user = UserInfo.objects.filter(uname=account)
        if user:
            pwd = user[0].pwd
            if pwd == password:
                request.session['user'] = user[0]
                cart = request.session.get('cart')
                if red == 'cart' and cart:
                    for k, v in cart.items():
                        goods = user[0].cartitem_set.filter(goods=v[0], color=v[1], size=v[2])
                        if goods:
                            goods.update(count=v[3])
                        else:
                            CartItem.objects.create(goods=v[0], color=v[1], size=v[2], count=v[3], user=user[0])
                    del request.session['cart']
                    return redirect('/cart/')
                return redirect('/user/usercenter/')
        return render(request, 'login.html', {'msg': '登录失败，账号或者密码错误'})
    elif request.method == 'GET':
        red = request.GET.get('redirect', '')
        return render(request, 'login.html', {'red': red})


def vcode(request):
    # r = request.GET.get('r', '')
    # 传递了一个时间戳 用来更改每次访问的url 以此来刷新验证码
    bgcolor = (random.randrange(20, 200), random.randrange(20, 200), random.randrange(20, 200))
    width = 100
    height = 36
    img = Image.new('RGB', (width, height), bgcolor)
    draw = ImageDraw.Draw(img)
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0abcdefghijklmnopqrstuvwxyz'
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    font = ImageFont.truetype('C:\Windows\Fonts\comic.ttf', 23)
    fontcolor = (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))
    # 绘制4个字
    draw.text((5, 0), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 0), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 0), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 0), rand_str[3], font=font, fill=fontcolor)
    del draw
    # 存入session，用于做进一步验证
    request.session['verifycode'] = rand_str
    # print('当前验证码是%s'%rand_str)
    buf = BytesIO()
    # 将图片保存在内存中，文件类型为png
    img.save(buf, 'png')
    # 将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')


def checkcode(request):
    code = request.GET.get('code', '')
    virefy =  request.session.get('verifycode', '')
    if virefy and virefy == code:
        return JsonResponse({'checkFlag': True})
    else:
        return JsonResponse({'checkFlag': False})


def register(request):
    if request.method == 'POST':
        account = request.POST.get('account', '')
        password = request.POST.get('password', '')
        user = UserInfo.objects.filter(uname=account)
        print(password)
        if not user:
            UserInfo.objects.create(uname=account, pwd=password)
            return redirect('/user/login/')
        return redirect('/user/register/')
    if request.method == "GET":
        return render(request, 'register.html')


def check_uname(request):
    if request.method == 'GET':
        flag = False
        uname = request.GET.get('uname', '')
        user = UserInfo.objects.filter(uname=uname)
        if user:
            flag = True
        return JsonResponse({'flag': flag})


def usercenter(request):
    return render(request, 'center.html')


def logout(request):
    if request.method == "POST":
        user = request.session.get('user', '')
        if user:
            # del request.session['user']
            request.session.clear()
    return JsonResponse({'flag': True})


def address(request):
    if request.method == "POST":
        provinceId = request.POST.get('provinceId', '')
        result = Area.objects.filter(parentid=int(provinceId))
        result = serializers.serialize('json', result)
        return JsonResponse({"citys": result})
    else:
        area = Area.objects.filter(parentid=0)
        return render(request, 'address.html', {'provinces': area})


def save_address(request):
    if request.method == "POST":
        address = request.POST.get('address', '')
        name = request.POST.get('name', '')
        phone = request.POST.get('phone', '')
        Address.objects.create(aname=name, aphone=phone, addr=address, user=request.session.get('user', ''))
        return JsonResponse({'flag': True})


def set_default(request):
    flag = False
    id = request.GET.get('id', '')
    user = request.session.get('user', '')
    # 如果此用户有这个地址
    addr = Address.objects.filter(id=id, user=user)
    if addr:
        Address.objects.filter(user=user).update(isdefault=False)
        addr[0].isdefault = True
        addr[0].save()
        flag = True
    return JsonResponse({'flag': flag})


def del_addr(request):
    flag = False
    id = request.GET.get('id', '')
    user = request.session.get('user', '')
    addr = Address.objects.filter(id=id, user=user)
    if addr:
        addr[0].delete()
        flag = True
    return JsonResponse({'flag': flag})


def addr(request):
    return render(request, 'addr.html')