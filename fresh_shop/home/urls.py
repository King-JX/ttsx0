
from django.conf.urls import url

from home import views

urlpatterns = [
    url(r'^login/', views.login, name='login'),
    url(r'^index/', views.index, name='index'),

]