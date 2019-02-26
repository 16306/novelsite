from django import forms
from django.contrib import auth
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username_or_email = forms.CharField(
        label='用户名', widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': '请输入用户名或邮箱'}
        )
    )
    password = forms.CharField(
        label='密码', widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': '请输入密码'}
        )
    )

    def clean(self):
        username_or_email = self.cleaned_data['username_or_email']
        password = self.cleaned_data['password']
        user = auth.authenticate(username=username_or_email, password=password)
        if user is None:
            if User.objects.filter(email=username_or_email).exists():
                username = User.objects.get(email=username_or_email).username
                user = auth.authenticate(username=username, password=password)
                if user is not None:
                    self.cleaned_data['user'] = user
                    return self.cleaned_data
            raise forms.ValidationError('用户名或密码不正确')
        else:
            self.cleaned_data['user'] = user
        return self.cleaned_data


class RegForm(forms.Form):
    username = forms.CharField(
        label='用户名', max_length=16, min_length=5, widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': '请输入5-16位用户名'}
        )
    )
    password = forms.CharField(
        label='密码', min_length=6, widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': '请输入至少6位密码'}
        )
    )
    password_again = forms.CharField(
        label='再次输入密码', min_length=6, widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': '请再次输入密码'}
        )
    )
    email = forms.CharField(
        label='邮箱', widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': '请输入邮箱'}
        )
    )

    code = forms.CharField(
        label='验证码: ', required=False, widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': '点击“发送验证码”发送到邮箱'}
        )
    )

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(RegForm, self).__init__(*args, **kwargs)

    def clean(self):
        code = self.request.session.get('register_code', '')
        user_code = self.cleaned_data.get('code', '')
        if not (code != '' and code == user_code):
            raise forms.ValidationError("验证码不正确")
        return self.cleaned_data

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('用户名已存在')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('email已存在')
        return email

    def clean_password_again(self):
        password = self.cleaned_data['password']
        password_again = self.cleaned_data['password_again']
        if password_again != password:
            raise forms.ValidationError('两次输入密码不一致')
        return password_again

    def clean_code(self):
        code = self.cleaned_data.get('code', '').strip()
        if code == '':
            raise forms.ValidationError("验证码不能为空")
        return code


class ChangeNikenameForm(forms.Form):
    nikename_new = forms.CharField(
        label='新昵称: ', max_length=16, widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': '请输入新昵称'}
        )
    )

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(ChangeNikenameForm, self).__init__(*args, **kwargs)

    def clean(self):
        if self.user.is_authenticated:
            self.cleaned_data['user'] = self.user
        else:
            raise forms.ValidationError('用户尚未登录')
        return self.cleaned_data

    def clean_nikename_new(self):
        nikename_new = self.cleaned_data.get('nikename_new', '').strip()
        if nikename_new == '':
            raise forms.ValidationError('新昵称不能为空')
        return nikename_new


class BindEmailForm(forms.Form):
    email = forms.EmailField(
        label='邮箱: ', widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '请输入有效的邮箱'})
    )
    code = forms.CharField(
        label='验证码: ', required=False, widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': '点击“发送验证码”发送到邮箱'}
        )
    )

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(BindEmailForm, self).__init__(*args, **kwargs)

    def clean(self):
        if self.request.user.is_authenticated:
            self.cleaned_data['user'] = self.request.user
        else:
            raise forms.ValidationError('用户尚未登录')
        if self.request.user.email != '':
            raise forms.ValidationError("已经绑定邮箱")
        code = self.request.session.get('bind_email_code', '')
        user_code = self.cleaned_data.get('code', '')
        if not (code != '' and code == user_code):
            raise forms.ValidationError("验证码不正确")
        return self.cleaned_data

    def clean_code(self):
        code = self.cleaned_data.get('code', '').strip()
        if code == '':
            raise forms.ValidationError("验证码不能为空")
        return code

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('email已绑定')
        return email


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(
        label='旧密码', widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': '请输入旧密码'}
        )
    )
    new_password = forms.CharField(
        label='新密码', widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': '请输入新密码'}
        )
    )
    new_password_again = forms.CharField(
        label='再次输入新密码', min_length=6, widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': '请再次输入新密码'}
        )
    )

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean(self):
        new_password = self.cleaned_data.get('new_password', '')
        new_password_again = self.cleaned_data.get('new_password_again', '')
        if new_password != new_password_again or new_password == '':
            raise forms.ValidationError('两次输入密码不一致')
        return self.cleaned_data

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password', '')
        if not self.user.check_password(old_password):
            raise forms.ValidationError('旧密码不正确')
        return old_password


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(
        label='邮箱: ', widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': '请输入绑定的邮箱'}
        )
    )
    code = forms.CharField(
        label='验证码: ', required=False, widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': '点击“发送验证码”发送到邮箱'}
        )
    )
    new_password = forms.CharField(
        label='新密码', min_length=6, widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': '请输入至少6位数的新密码'}
        )
    )

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(ForgotPasswordForm, self).__init__(*args, **kwargs)

    def clean_username(self):
        email = self.cleaned_data['email'].strip()
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱不存在')
        return email

    def clean_code(self):
        code = self.cleaned_data.get('code', '').strip()
        if code == '':
            raise forms.ValidationError("验证码不能为空")

        code = self.request.session.get('forgot_password_code', '')
        user_code = self.cleaned_data.get('code', '')
        if not (code != '' and code == user_code):
            raise forms.ValidationError("验证码不正确")
        return code
