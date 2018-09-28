from django.conf.urls import url
from cart import views

app_name = 'cart'
urlpatterns = [
    url(r'^$', views.index),
]
