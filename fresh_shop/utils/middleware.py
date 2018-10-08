import re

from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseRedirect

from users.models import User
from cart.models import ShoppingCart


class UserAuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        # 登录验证得中间件
        # 不需要验证的地址
        not_need_check = ['/home/index/', '/users/login/','/cart/delete_goods/',
                          '/users/register/', '/cart/check/', '/cart/cart/',
                          '/cart/f_price/', '/cart/add_cart/',
                          '/media/(.*)/', '/static/(.*)', '/cart/cart_count/',
                          '/goods/goods_detail/(\d+)/']
        path = request.path
        for not_path in not_need_check:
            if re.match(not_path, path):
                return None

        user_id = request.session.get('user_id')
        if not user_id:
            return HttpResponseRedirect(reverse('users:login'))

        user = User.objects.get(pk=user_id)
        request.user = user
        return None


class UserSessionMiddleware(MiddlewareMixin):

    def process_request(self, request):
        user_id = request.session.get('user_id')
        if user_id:
            session_goods = request.session.get('goods')
            if session_goods:
                for goods in session_goods:
                    cart = ShoppingCart.objects.filter(goods_id=goods[0],
                                                user_id=user_id).first()
                    if cart:
                        if cart.nums != goods[1]:
                            cart.nums = int(goods[1])
                        cart.is_select = int(goods[2])
                        cart.save()
                    else:
                        ShoppingCart.objects.create(user_id=user_id,
                                                    goods_id=goods[0],
                                                    nums=int(goods[1]),
                                                    is_select=int(goods[2]))
                return None