
from django.conf.urls import url

from goods import views

urlpatterns = [
    url(r'^goods_detail/(\d+)/', views.goods_detail, name='goods_detail')
]