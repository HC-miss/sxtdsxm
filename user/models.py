from django.db import models


class Area(models.Model):
    areaid = models.IntegerField(primary_key=True)
    areaname = models.CharField(max_length=50)
    parentid = models.IntegerField()
    arealevel = models.IntegerField()
    status = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'area'
        unique_together = (('areaid', 'parentid'),)


class Address(models.Model):
    aname = models.CharField(max_length=30)
    aphone = models.CharField(max_length=11)
    addr = models.CharField(max_length=100)
    isdefault = models.BooleanField(default=False)
    user = models.ForeignKey('UserInfo', on_delete=models.CASCADE)

    def __str__(self):
        return self.aname


class UserInfo(models.Model):
    uname = models.CharField(max_length=100)
    pwd = models.CharField(max_length=100)

    def __str__(self):
        return self.uname
