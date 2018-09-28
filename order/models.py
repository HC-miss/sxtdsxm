from django.db import models
from user.models import *
from goods.models import *


class Order(models.Model):
    order_num = models.CharField(max_length=50)
    out_trade_num = models.CharField(max_length=30)
    trade_no = models.CharField(max_length=120)
    status = models.CharField(max_length=20)
    pay_way = models.CharField(max_length=20)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.uname


class OrderItem(models.Model):
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    count = models.PositiveIntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
