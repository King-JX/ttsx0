from django.shortcuts import render
from django.http import JsonResponse

from goods.models import Goods
from cart.models import ShoppingCart


def add_cart(request):
    if request.method =='POST':
        # 添加购物车, 分登录和未登录情况
        # 判断用户是否登录session['user_id']
        # 1. 没有登陆的情况

        # 1.1 添加到购物车的数据,就是添加到session中
        # 1.2 如果商品已经加入到session中,则修改session中的商品个数
        # 1.3 如果商品没有添加到session中, 则添加

        goods_id = request.POST.get('goods_id')
        goods_num = request.POST.get('goods_num')

        goods_list = [goods_id, goods_num, 1]
        if request.session.get('goods'):
            flag = 0
            session_goods = request.session['goods']
            for goods in session_goods:
                if goods_id == goods[0]:
                    goods[1] = str(int(goods[1]) + int(goods_num))
                    flag = 1
            if not flag:
                session_goods.append(goods_list)
            request.session['goods'] = session_goods
            cart_count = len(session_goods)
        else:
            data = []
            data.append(goods_list)
            request.session['goods'] = data
            cart_count = 1

        return JsonResponse({'code': 200, 'cart_count': cart_count})


def cart(request):
    if request.method == 'GET':
        user_id = request.session.get('user_id')
        if user_id:
            shop_cart = ShoppingCart.objects.filter(user_id=user_id)
            goods_all = [(cart.goods, cart.is_select, cart.nums) for cart in shop_cart]
            return render(request, 'cart.html', {'goods_all': goods_all})
        else:
            session_goods = request.session.get('goods')
            if session_goods:
                goods_all = [(Goods.objects.get(pk=good[0]), good[2], good[1])
                             for good in session_goods]
            else:
                goods_all = ''
            return render(request, 'cart.html', {'goods_all': goods_all})


def f_price(request):
    user_id = request.session.get('user_id')
    if user_id:
        carts = ShoppingCart.objects.filter(user_id=user_id)
        cart_data = {}
        cart_data['goods_price'] = [(cart.goods_id, cart.nums * cart.goods.shop_price)
                                    for cart in carts]
        all_price = 0
        for cart in carts:
            all_price += cart.nums * cart.goods.shop_price
        cart_data['all_price'] = all_price
    else:
        session_goods = request.session.get('goods')
        cart_data = {}
        data_all = []
        all_price = 0
        for goods in session_goods:
            data = []
            data.append(goods[0])
            g = Goods.objects.get(pk=goods[0])
            data.append(int(goods[1]) * g.shop_price)
            data_all.append(data)
            if goods[2]:
                all_price += int(goods[1]) * g.shop_price
        cart_data['goods_price'] = data_all
        cart_data['all_price'] = all_price
    return JsonResponse({'code': 200, 'cart_data': cart_data})


def check(request):
    if request.method == 'POST':
        goods_id = request.POST.get('goods_id')
        session_goods = request.session['goods']
        data = []
        for goods in session_goods:
            if goods_id == goods[0]:
                if goods[2]:
                    goods[2] = False
                else:
                    goods[2] = True
            data.append(goods)
        if data:
            request.session['goods'].clear()
            request.session['goods'] = data
            return JsonResponse({'code': 200, 'goods': session_goods})
        else:
            shop_cart = ShoppingCart.objects.filter(id=goods_id).first()
            if shop_cart.is_select:
                shop_cart.is_select = False
            else:
                shop_cart.is_select = True
            shop_cart.save()
            return JsonResponse({'code': 200, 'msg': '请求成功'})


def ChangeSessionGoods(request):
    if request.method == 'POST':
        goods_id = request.POST.get('goods_id')
        goods_num = request.POST.get('goods_num')
        goods = request.session.get('goods')
        for session_goods in goods:
            if session_goods[0] == goods_id:
                session_goods[1] = int(session_goods[1]) + int(goods_num)
        user_id = request.session.get('user_id')

        if user_id:
            shop_cart = ShoppingCart.objects.filter(user_id=user_id, goods_id=goods_id).first()
            shop_cart.nums = goods_num
            shop_cart.save()
        return JsonResponse({'code': 200, 'msg': '请求成功'})