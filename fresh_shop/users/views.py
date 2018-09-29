from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from users.forms import UserForm, UserLogin
from users.models import User


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['user_name']
            password = make_password(form.cleaned_data['pwd'])
            email = form.cleaned_data['email']
            User.objects.create(username=username, password=password, email=email)
            return HttpResponseRedirect(reverse('users:login'))
        else:
            return render(request, 'register.html', {'form': form})


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        form = UserLogin(request.POST)
        if form.is_valid():

            user = User.objects.filter(username=form.cleaned_data['username']).first()
            if not check_password(form.cleaned_data['pwd'], user.password):
                return HttpResponseRedirect(reverse('users:login'))
            # 添加登录成功得验证
            request.session['user_id'] = user.id
            return HttpResponseRedirect(reverse('home:index'))
        else:
            return render(request, 'login.html', {'form': form})


def base_main(request):
    if request.method == 'GET':
        user_id = request.session.get('user_id')
        user = User.objects.filter(id=user_id).first()
        return render(request, 'base_main.html', {'user': user})
