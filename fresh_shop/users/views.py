from django.contrib.auth.hashers import make_password, check_password
from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse

from users.forms import UserForm, UserLogin
from users.models import User, UserAddress
from orders.models import  OrderInfo


PAGE_NUMBER = 3


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



def is_login(request):
    if request.method == 'GET':
        user = request.user
        return JsonResponse({'code': 200, 'msg': '请求成功', 'username': user.username})


def logout(request):
    if request.method == 'GET':
        request.session.flush()
        return HttpResponseRedirect(reverse('home:index'))


def user_center_info(request):
    if request.method == 'GET':
        user = request.session.get('user_id')
        user = User.objects.filter(id=user).first()
        return render(request, 'user_center_info.html', {'user': user})


def user_center_order(request):
    if request.method == 'GET':
        user = request.user
        # 获取分页
        try:
            # 如果page参数不能转化为int类型，则异常，默认page为1
            page = int(request.GET.get('page', 1))
        except:
            page = 1
        orders = OrderInfo.objects.filter(user=user)
        paginator = Paginator(orders, PAGE_NUMBER)
        orders = paginator.page(page)
        order_status = OrderInfo.ORDER_STATUS
        return render(request, 'user_center_order.html', {'orders': orders,
                                                          'order_status': order_status})


def user_center_site(request):
    if request.method == 'GET':
        user = request.user
        user_addresses = UserAddress.objects.filter(user=user).order_by('-id')
        return render(request, 'user_center_site.html', {'user_addresses': user_addresses})
    if request.method == 'POST':
        name = request.POST.get('name')
        site_area = request.POST.get('site_area')
        mail = request.POST.get('mail')
        phone = request.POST.get('phone')
        user_id = request.session.get('user_id')
        UserAddress.objects.create(address=site_area, signer_mobile=phone,
                                   signer_postcode=mail, signer_name=name,
                                   user_id=user_id)
        return HttpResponseRedirect(reverse('users:user_center_site'))