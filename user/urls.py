from django.conf.urls import url
from . import views

app_name = 'user'
urlpatterns = [
    url(r'^login/$', views.login),
    url(r'^logout/$', views.logout),
    url(r'^address/$', views.address),
    url(r'^save_address/$', views.save_address),
    url(r'^set_default/$', views.set_default),
    url(r'^del_addr/$', views.del_addr),
    url(r'^register/$', views.register),
    url(r'^vcode/$', views.vcode),
    url(r'^checkcode/$', views.checkcode),
    url(r'^check_uname/$', views.check_uname),
    url(r'^usercenter/$', views.usercenter),
    url(r'^addr/$', views.addr),
]
