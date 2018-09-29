from django.shortcuts import render

from goods.models import Goods, GoodsCategory


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        pass


def index(request):
    if request.method == 'GET':
        category_types = GoodsCategory.CATEGORY_TYPE
        goods = Goods.objects.all().order_by('-id')
        data_all = {}
        for type in category_types:
            data = []
            count = 0
            for good in goods:
                if count < 4:
                    if type[0] == good.category.category_type:
                        data.append(good)
                        count += 1
            data_all['goods_'+str(type[0])] = data

        return render(request, 'index.html', {'data_all': data_all,
                                              'category_types':category_types})


        # goods = Goods.objects.all()
        # categorys = GoodsCategory.objects.all()
        # category_types = GoodsCategory.CATEGORY_TYPE
        # return render(request, 'index.html', {'goods': goods,
        #                                       'category_types': category_types,
        #                                       'categorys': categorys})