from django.shortcuts import render
from django.http import JsonResponse

from cart.models import ShoppingCart
from orders.models import OrderGoods, OrderInfo
from users.models import UserAddress
from utils.functions import get_order_sn


def order(request):
    if request.method == 'GET':
        user_id = request.session['user_id']
        # user = request.user
        cart_goods = ShoppingCart.objects.filter(user_id=user_id, is_select=True)
        total_num = 0
        total_price = 0
        for cart in cart_goods:
            cart.total_price = cart.nums * cart.goods.shop_price
            total_num += cart.nums
            total_price += cart.total_price
        return render(request, 'place_order.html', {'cart_goods': cart_goods,
                                                    'total_num': total_num,
                                                    'total_price': total_price})

    if request.method == 'POST':

        user_id = request.session.get('user_id')
        address_id = request.POST.get('address_id')
        user_address = UserAddress.objects.filter(id=address_id).first()
        carts = ShoppingCart.objects.filter(user_id=user_id, is_select=True)
        order_sn = get_order_sn()
        order_mount = 0
        for cart in carts:
            order_mount += cart.nums * cart.goods.shop_price
        order = OrderInfo.objects.create(user_id=user_id,
                                        order_sn=order_sn,
                                        order_mount=order_mount,
                                        address=user_address.address,
                                        signer_name=user_address.signer_name,
                                        signer_mobile=user_address.signer_mobile)
        for cart in carts:
            OrderGoods.objects.create(order_id=order.id,
                                      goods_id=cart.goods_id,
                                      goods_nums=cart.nums)
        carts.delete()
        request.session.pop('goods')
        return JsonResponse({'code': 200, 'msg':'请求成功'})
