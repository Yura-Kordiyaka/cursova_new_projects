from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.shortcuts import redirect, reverse
# Create your views here.
from .models import User
from .utilits import validate_password
from django.contrib import messages


def login_user(request):
    if request.method == "GET":
        return render(request, 'backend/login.html')
    elif request.method == "POST":
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)
            return redirect('main')
        else:
            messages.error(request, 'неправильний логін або пароль')
            return redirect('login_user')


def authorization_user(request):
    if request.method == "GET":
        return render(request, 'backend/authorization.html')
    elif request.method == "POST":
        if User.objects.filter(username=request.POST['username']).exists():
            messages.error(request, 'користувач з таким нікнеймом вже існує')
            return redirect('authorization')
        if User.objects.filter(email=request.POST['email']).exists():
            messages.error(request, 'користувач з такою поштую вже існує')
            return redirect('authorization')
        if validate_password(request.POST['password']) == False:
            messages.error(request, 'Пароль не повинен містити пробілів')
            messages.error(request, 'Пароль повинен мати хоча б одну цифру')
            messages.error(request, 'пароль повинен містити хоча б одну велику букву')
            messages.error(request, 'Пароль повинен містити хоча б одну малу букву')
            messages.error(request, 'Пароль повинен мати більше ніж 8 символів')
            return redirect('authorization')
        else:
            user = User.objects.create_user(username=request.POST['username'], password=request.POST['password'],email=request.POST['email'])
            user.last_name = request.POST['last_name']
            user.first_name = request.POST['first_name']
            user.save()
            return redirect('login_user')
