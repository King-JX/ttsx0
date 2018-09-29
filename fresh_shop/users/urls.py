from django.conf.urls import url

from users import views

urlpatterns = [
    url(r'^register/', views.register, name='register'),
    url(r'^login/', views.login, name='login'),
    url(r'^base_main/', views.base_main, name='base_main')
]