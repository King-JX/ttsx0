# -*- coding: utf-8 -*-
# @File  : urls.py
# @Author: KingJX
# @Date  : 2018/9/25 15:20
""""""

from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from goods import views


urlpatterns = [
    url(r'^goods_category_list/', login_required(views.goods_category_list), name='goods_category_list'),
    url(r'^goods_category_detail/(\d+)/', login_required(views.goods_category_detail), name='goods_category_detail'),
    url(r'^goods_desc/(\d+)/', login_required(views.goods_desc), name='goods_desc'),
    url(r'^goods_detail/(\d+)/', login_required(views.goods_detail), name='goods_detail'),
    url(r'^goods_list/', login_required(views.goods_list), name='goods_list'),
    url(r'^order_list/', login_required(views.order_list), name='order_list'),
    url(r'^user_list/', login_required(views.user_list), name='user_list'),
    url(r'^goods_delete/(\d+)/', login_required(views.goods_delete), name='goods_delete'),

]


if __name__ == '__main__':
    pass
