# accounts/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseBadRequest
from django.views.decorators.http import (
    require_http_methods,
    require_safe,
    require_POST
)
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth import get_user_model
from django.contrib import auth
from .forms import UserCreationForm
User = get_user_model()


# Create your views here.
@require_http_methods(['GET', 'POST'])
def signup(request):
    if request.user.is_authenticated:
        return HttpResponseBadRequest('이미 로그인 하였습니다.')

    if request.method == 'POST':
        print('회원 가입요청중')
        form = UserCreationForm(request.POST)
        if form.is_valid():
            print('폼요청 성공')
            user = form.save()
            auth_login(request, user)
            return redirect('board:index')
    else:
        print('폼 요청 실패')
        form = UserCreationForm()
    context = {'form': form}
    return render(request, 'accounts/signup.html', context)


@require_http_methods(['GET', 'POST'])
def login(request):
    if request.user.is_authenticated:
        return HttpResponseBadRequest('이미 로그인 하였습니다.')

    if request.method == "POST":
        print('AuthenticationForm 생성 전')
        form = AuthenticationForm(request, request.POST)
        print('AuthenticationForm 생성됨')
        if form.is_valid():
            print('form 유효성 검사 통과')
            user = form.get_user()
            auth_login(request, user)
            return redirect('board:index')
    else:
        form = AuthenticationForm()
    context = {'form': form}
    print('form context 생성 및 전송 직전')
    return render(request, 'accounts/login.html', context)

