from django.conf.urls import url

from cart import views

urlpatterns = [
    url(r'^add_cart/', views.add_cart, name='add_cart'),
    url(r'^cart/', views.cart, name='cart'),
    url(r'^f_price/', views.f_price, name='f_price'),
    url(r'^check/', views.check, name='check'),
    url(r'change_session_goods/', views.ChangeSessionGoods, name='change_session_goods'),

]