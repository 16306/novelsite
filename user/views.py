import string
import random
import time
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.mail import send_mail
from .forms import LoginForm, RegForm, ChangeNikenameForm, BindEmailForm, ChangePasswordForm, ForgotPasswordForm
from .models import Collection, Profile


def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('home')))
    else:
        login_form = LoginForm()
    context = {'login_form': login_form}
    return render(request, 'user/login.html', context)


def register(request):
    if request.method == 'POST':
        register_form = RegForm(request.POST, request=request)
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            email = register_form.cleaned_data['email']
            password = register_form.cleaned_data['password']
            user = User.objects.create_user(username, email, password)
            user.save()
            del request.session['register_code']
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('home')))
    else:
        register_form = RegForm()
    context = {'register_form': register_form}
    return render(request, 'user/register.html', context)


def logout(request):
    auth.logout(request)
    return redirect(request.GET.get('from', reverse('home')))


def user_info(request):
    context = {}
    return render(request, 'user/user_info.html', context)


def app_collection(request, info):
    collection = Collection()
    collection.user = request.user
    collection.collection = request.GET.get('from', '')
    collection.info = info
    collection.save()
    return redirect(request.GET.get('from', reverse('home')))


def show_collection(request):
    user = request.user
    context = {'collections': Collection.objects.filter(user=user)}
    return render(request, 'user/collection.html', context)


def change_nikename(request):
    redirect_to = request.GET.get('from', reverse('home'))
    if request.method == 'POST':
        form = ChangeNikenameForm(request.POST, user=request.user)
        if form.is_valid():
            nikename_new = form.cleaned_data['nikename_new']
            profile, created = Profile.objects.get_or_create(user=request.user)
            profile.nikename = nikename_new
            profile.save()
            return redirect(redirect_to)
    else:
        form = ChangeNikenameForm()
    context = {
        'form': form,
        'page_title': '修改昵称',
        'form_title': '修改昵称',
        'submit_text': '修改',
        'return_back': redirect_to
    }
    return render(request, 'form.html', context)


def bind_email(request):
    redirect_to = request.GET.get('from', reverse('home'))
    if request.method == 'POST':
        form = BindEmailForm(request.POST, request=request)
        if form.is_valid():
            email = form.cleaned_data['email']
            request.user.email = email
            request.user.save()
            del request.session['bind_email_code']
            return redirect(redirect_to)
    else:
        form = BindEmailForm()
    context = {
        'form': form,
        'page_title': '绑定邮箱',
        'form_title': '绑定邮箱',
        'submit_text': '绑定',
        'return_back': redirect_to
    }
    return render(request, 'user/bind_email.html', context)


def send_code(request):
    email = request.GET.get('email', '')
    send_for = request.GET.get('send_for', '')
    data = {}
    if email != '':
        code = ''.join(random.sample(string.ascii_letters + string.digits, 4))
        now = int(time.time())
        send_code_time = request.session.get('send_code_time', 0)
        if now - send_code_time < 30:
            data['status'] = 'ERROR'
        else:
            request.session[send_for] = code
            request.session['send_code_time'] = now
            send_mail(
                '邮箱相关',
                '验证码：{}'.format(code),
                '1490585475@qq.com',
                [email],
                fail_silently=False,
            )
            data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)


def change_password(request):
    redirect_to = request.GET.get('from', reverse('home'))
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST, user=request.user)
        if form.is_valid():
            user = request.user
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password']
            user.set_password(new_password)
            user.save()
            auth.logout(request)
            return redirect(redirect_to)
    else:
        form = ChangePasswordForm()
    context = {
        'form': form,
        'page_title': '修改密码',
        'form_title': '修改密码',
        'submit_text': '修改',
        'return_back': redirect_to
    }
    return render(request, 'form.html', context)


def forgot_password(request):
    redirect_to = request.GET.get('from', reverse('home'))
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST, request=request)
        if form.is_valid():
            email = form.cleaned_data['email']
            new_password = form.cleaned_data['new_password']
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            del request.session['forgot_password_code']
            return redirect(redirect_to)
    else:
        form = ForgotPasswordForm()
    context = {
        'form': form,
        'page_title': '重置密码',
        'form_title': '重置密码',
        'submit_text': '重置',
        'return_back': redirect_to
    }
    return render(request, 'user/forgot_password.html', context)