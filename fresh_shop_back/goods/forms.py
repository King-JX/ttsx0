# -*- coding: utf-8 -*-
# @File  : forms.py
# @Author: KingJX
# @Date  : 2018/9/26 9:24
""""""


from django import forms

from goods.models import GoodsCategory


class GoodsForm(forms.Form):
    name = forms.CharField(required=True)
    goods_sn = forms.CharField(required=True)
    category = forms.CharField(required=True)
    goods_nums = forms.CharField(required=True)
    market_price = forms.CharField(required=True)
    shop_price = forms.CharField(required=True)
    goods_brief = forms.CharField(required=True)
    goods_front_image = forms.ImageField(required=False)

    def clean_category(self):
        # 验证字段, 返回category对象
        category_id = self.cleaned_data['category']
        category = GoodsCategory.objects.filter(category_type=category_id).first()
        if category:
            return category



