from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import LoginForm



def index(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                if user.profile.role == 'student':
                    return redirect('/user/')
                elif user.profile.role == 'chef':
                    return redirect('/chef/')
                elif user.profile.role == 'moderator':
                    return redirect('/moderator/')
            else:
                messages.error(request, 'Неверный логин или пароль')
        messages.error(request, 'Неверный логин или пароль')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/menu/')