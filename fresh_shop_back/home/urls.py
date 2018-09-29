# -*- coding: utf-8 -*-
# @File  : urls.py
# @Author: KingJX
# @Date  : 2018/9/25 9:59
""""""

from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from home import views

urlpatterns = [
    url(r'^login/', views.login, name='login'),
    url(r'^index/', login_required(views.index) , name='index'),
    url(r'^logout/', login_required(views.logout), name='logout'),

]

if __name__ == '__main__':
    pass
