from django.conf.urls import url

from cart import views

urlpatterns = [
    url(r'^add_cart/', views.add_cart, name='add_cart'),
    url(r'^cart/', views.cart, name='cart'),
    url(r'^f_price/', views.f_price, name='f_price'),
    url(r'^check/', views.check, name='check'),
    url(r'^change_session_goods/', views.change_session_goods, name='change_session_goods'),
    url(r'^cart_count/', views.cart_count, name='cart_count'),
    url(r'^delete_goods/', views.delete_goods, name='delete_goods'),

]