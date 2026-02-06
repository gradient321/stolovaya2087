from django.shortcuts import render, redirect
from moderator.form import RegisterForm
from django.contrib import messages
from django.contrib.auth.models import User
from menu.models import *


def index(request):

    if request.method == 'POST':
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']

            if User.objects.filter(username=username).exists():
                messages.error(request, 'Пользователь с таким логином уже существует')
            else:
                user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name, email=email)
                profile = Profile.objects.create(user=user)
                user.save()
                profile.save()
                return redirect('/login/')


    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})
