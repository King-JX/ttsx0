
from django import forms

from users.models import User


class UserForm(forms.Form):
    user_name = forms.CharField(required=True, error_messages={'required':'用户名必填'})
    pwd = forms.CharField(required=True, error_messages={'required':'密码必填'})
    cpwd = forms.CharField(required=True, error_messages={'required':'密码必填'})
    email = forms.CharField(required=True, error_messages={'required':'邮箱必填'})
    allow = forms.BooleanField(required=True)

    def clean(self):
        username = self.cleaned_data.get('user_name')
        pwd = self.cleaned_data.get('pwd')
        cpwd = self.cleaned_data.get('cpwd')
        # 校验用户名是否存在
        user = User.objects.filter(username=username)
        if user:
            raise forms.ValidationError({'user_name': '用户名已存在'})
        if pwd != cpwd:
            raise forms.ValidationError({'cpwd': '两次密码不同'})
        return self.cleaned_data


class UserLogin(forms.Form):
    username = forms.CharField(required=True, error_messages={'required':'用户名必填'})
    pwd = forms.CharField(required=True, error_messages={'required':'密码必填'})

    def clean_username(self):
        username = self.cleaned_data.get('username')
        user = User.objects.filter(username=username)
        if not user:
            raise forms.ValidationError({'username': '该用户不存'})
        return username