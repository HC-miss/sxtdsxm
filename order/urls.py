from django.conf.urls import url
from order import views

app_name = 'order'
urlpatterns = [
    url(r'^$', views.index),
    url(r'^orderlist', views.orderlist),
    url(r'^toorder/$', views.toorder),
    url(r'^checkpay/$', views.checkpay),
]