from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from goods.models import GoodsCategory, Goods
from goods.forms import GoodsForm



PAGE_NUMBER = 5


def goods_category_list(request):
    if request.method == 'GET':
        # 获取分类信息
        categorys = GoodsCategory.objects.all()
        # 返回类型
        category_types = GoodsCategory.CATEGORY_TYPE
        return render(request, 'goods_category_list.html',
                      {'categorys':categorys,
                       'category_types': category_types})


def goods_category_detail(request, id):
    if request.method == 'GET':
        category = GoodsCategory.objects.get(pk=id)
        category_types = GoodsCategory.CATEGORY_TYPE
        return render(request, 'goods_category_detail.html',
                      {'category': category,
                      'category_types': category_types})

    if request.method == 'POST':
        category_front_image = request.FILES.get('category_front_image')
        if category_front_image:
            category = GoodsCategory.objects.get(pk=id)
            category.category_front_image = category_front_image
            category.save()
        return HttpResponseRedirect(reverse('goods:goods_category_list'))


def goods_desc(request, id):
    if request.method == 'GET':
        goods = Goods.objects.get(pk=id)
        return render(request, 'goods_desc.html', {'goods': goods})
    if request.method == 'POST':
        content = request.POST.get('content')
        Goods.objects.filter(pk=id).update(goods_desc=content)
        return HttpResponseRedirect(reverse('goods:goods_list'))


def goods_detail(request, id):
    if request.method == 'GET':
        categorys = GoodsCategory.CATEGORY_TYPE
        if id=='0':
            return render(request, 'goods_detail.html', {'categorys': categorys})
        else:
            good = Goods.objects.get(pk=id)
            return render(request, 'goods_detail.html', {'good': good, 'categorys': categorys})
    if request.method == 'POST':
        form = GoodsForm(request.POST, request.FILES)
        if form.is_valid():
            if id=='0':
                data = form.cleaned_data
                Goods.objects.create(**data)
                return HttpResponseRedirect(reverse('goods:goods_list'))
            else:
                data = form.cleaned_data
                goods_front_image = data.pop('goods_front_image')
                if goods_front_image:
                    goods = Goods.objects.filter(pk=id).first()
                    goods.goods_front_image = goods_front_image
                    goods.save()
                Goods.objects.filter(pk=id).update(**data)
                return HttpResponseRedirect(reverse('goods:goods_list'))
        else:
            return render(request, 'goods_detail.html')

            # name = request.POST.get('name')
            # goods_sn = request.POST.get('goods_sn')
            # category = GoodsCategory.objects.filter(category_type=int(request.POST.get('category'))).first()
            # goods_nums = request.POST.get('goods_nums')
            # market_price = request.POST.get('market_price')
            # shop_price = request.POST.get('shop_price')
            # goods_brief = request.POST.get('goods_brief')
            # goods_front_image = request.FILES.get('goods_front_image')
            # Goods.objects.create(name=name, category=category, goods_sn=goods_sn,
            #                      goods_nums=goods_nums, market_price=market_price,
            #                      shop_price=shop_price, goods_brief=goods_brief,
            #                      goods_front_image=goods_front_image)



def goods_list(request):
    if request.method == 'GET':
        goods = Goods.objects.all()
        page_num = int(request.GET.get('page', 1))
        page = Paginator(goods, PAGE_NUMBER).page(page_num)
        category_types = GoodsCategory.CATEGORY_TYPE
        return render(request, 'goods_list.html', {'goods': goods,
                                                   'category_types': category_types,
                                                   'page': page})


def goods_delete(request, id):
    if request.method == 'GET':
        Goods.objects.filter(pk=id).delete()
        return HttpResponseRedirect(reverse('goods:goods_list'))
    if request.method == 'POST':
        Goods.objects.filter(pk=id).delete()
        return JsonResponse({'code': 200, 'msg': '请求成功'})



def order_list(request):
    if request.method == 'GET':
        return render(request, 'order_list.html')


def user_list(request):
    if request.method == 'GET':
        return render(request, 'user_list.html')
