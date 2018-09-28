from goods.models import *
from django.db import models
from user.models import UserInfo


class CartItem(models.Model):
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    count = models.PositiveIntegerField()
    isdelete = models.BooleanField(default=False)
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)

    def __str__(self):
        return '%s购买的商品:%s'%(self.user.uname, self.goods.gname)
