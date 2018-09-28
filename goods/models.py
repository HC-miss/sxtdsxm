from django.db import models
from django.db.models import Count
import collections


class Category(models.Model):
    cname = models.CharField(max_length=10)

    def __str__(self):
        return self.cname


class Goods(models.Model):
    gname = models.CharField(max_length=100)
    gdesc = models.CharField(max_length=100)
    oldprice = models.DecimalField(max_digits=5, decimal_places=2)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.gname

    def get_img(self):
        return self.inventory_set.first().color.colorurl

    def get_size(self):
        inventory = self.inventory_set.all().order_by('size')
        sizes = []
        for i in inventory:
            if i.size not in sizes:
                sizes.append(i.size)
        return sizes

    def get_color(self):
        inventory = self.inventory_set.all()
        color = []
        for i in inventory:
            if i.color not in color:
                color.append(i.color)
        return color

    def get_detail_info(self):
        datas = collections.OrderedDict()
        goods_detail = self.goodsdetail_set.all()
        for detail in goods_detail:
            gdname = detail.get_detail_name()
            if not datas.get(gdname, ''):
                datas[gdname] = [detail.gdurl]
            else:
                datas[gdname].append(detail.gdurl)
        return datas

class GoodsDetailName(models.Model):
    gdname = models.CharField(max_length=30)

    def __str__(self):
        return self.gdname


class GoodsDetail(models.Model):
    gdurl = models.ImageField(upload_to='')
    gdname = models.ForeignKey(GoodsDetailName, on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)

    def __str__(self):
        return '%s,%s'%(self.goods, self.gdname)

    def get_detail_name(self):
        return self.gdname.gdname


class Size(models.Model):
    sname = models.CharField(max_length=10)

    def __str__(self):
        return self.sname

class Color(models.Model):
    colorname = models.CharField(max_length=10)
    colorurl = models.ImageField(upload_to='color/')

    def __str__(self):
        return self.colorname


class Inventory(models.Model):
    count = models.PositiveIntegerField()
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)

    def __str__(self):
        return '%s %s'%(self.goods.gname, self.count)
