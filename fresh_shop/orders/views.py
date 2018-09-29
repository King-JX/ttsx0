from django.shortcuts import render
from django.http import JsonResponse

from cart.models import ShoppingCart
from orders.models import OrderGoods, OrderInfo
from utils.functions import get_order_sn


def order(request):
    if request.method == 'GET':
        user_id = request.session['user_id']
        # user = request.user
        cart_goods = ShoppingCart.objects.filter(user_id=user_id, is_select=True)
        for cart in cart_goods:
            cart.total_price = cart.nums * cart.goods.shop_price
        return render(request, 'place_order.html', {'cart_goods': cart_goods})

    if request.method == 'POST':

        user_id = request.session.get('user_id')
        carts = ShoppingCart.objects.filter(user_id=user_id, is_select=True)
        order_sn = get_order_sn()
        order_mount = 0
        for cart in carts:
            order_mount += cart.nums * cart.goods.shop_price
        order = OrderInfo.objects.create(user_id=user_id,
                                 order_sn=order_sn,
                                 order_mount=order_mount)
        for cart in carts:
            OrderGoods.objects.create(order_id=order.id,
                                      goods_id=cart.goods_id,
                                      goods_nums=cart.nums)
        carts.delete()
        request.session.pop('goods')
        return JsonResponse({'code': 200, 'msg':'请求成功'})
