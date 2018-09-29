# -*- coding: utf-8 -*-
# @File  : forms.py
# @Author: KingJX
# @Date  : 2018/9/25 10:31
""""""

from django import forms


class UserLoginForm(forms.Form):

    username = forms.CharField(required=True,
                               error_messages={
                                   'required': '账号必填'
                               })
    password = forms.CharField(required=True,
                               error_messages={
                                   'required': '密码必填'
                               })



if __name__ == '__main__':
    pass
