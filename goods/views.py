import math
from django.core.paginator import Paginator
from django.shortcuts import render
from goods.models import *


def index(request, pid=8, num=1):
    pid = int(pid)
    num = int(num)
    category = Category.objects.all()
    goods = Goods.objects.filter(category_id=pid).order_by('id')
    paginator = Paginator(goods, 8)

    if num < 1:
        num = 1
    if num > paginator.num_pages:
        num = paginator.num_pages

    page = paginator.page(num)
    start = (num - int(math.ceil(10.0 / 2)))

    if start < 1:
        start = 1
    end = start + 9

    if end > paginator.num_pages:
        end = paginator.num_pages

    if end <= 10:
        start = 1
    else:
        start = end - 9
    page_range = range(start, end+1)
    return render(request, 'index.html', {
        'categorys': category, 'pid': pid, 'goods': page, 'page_range': page_range, 'currentNum': num
    })


def recommend(func):
    def wraper(request, id, *args, **kwargs):
        c_list = request.COOKIES.get('c_recommend', '')
        goods_list = [i for i in c_list.split() if i.strip()]
        if Goods.objects.filter(pk=id):
            if id in goods_list:
                goods_list.remove(id)
                goods_list.insert(0, id)
            else:
                goods_list.insert(0, id)
        # 不展示正在浏览的和不属于当前浏览分类的
        goods_obj_list = [Goods.objects.get(id=i) for i in goods_list if
                          i != id and Goods.objects.get(id=id).category_id == Goods.objects.get(
                              id=i).category_id][:4]
        response = func(request, id, goods_obj_list, *args, **kwargs)
        response.set_cookie('c_recommend', ' '.join(goods_list),max_age=3*24*60*60)
        return response
    return wraper

@recommend
def detail(request, id=4, goods_obj_list=[]):
    id = int(id)
    goods = Goods.objects.filter(pk=id)
    if goods:
        goods = goods[0]
    else:
        # 如果查询商品详情不存在 则显示第一个商品的详情 也可以直接打印错误信息
        goods = Goods.objects.first()
    return render(request, 'detail.html', {'goods': goods, 'goods_obj_list': goods_obj_list})


def search(request):
    return HttpResponse('ok')