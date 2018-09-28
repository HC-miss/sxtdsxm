from django.conf.urls import url
from . import views

app_name = 'goods'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^detail/(\d+)$', views.detail, name='detail'),
    url(r'^category/(\d+)$', views.index),
    url(r'^category/(\d+)/page/(\d+)$', views.index),
    url(r'^search/$', views.search),
]
