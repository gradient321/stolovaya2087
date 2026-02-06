from django.shortcuts import render
from django.contrib.auth import logout
from menu.models import *
from django.shortcuts import redirect
from moderator.form import *



def profile(request):
    user = User.objects.select_related('profile').filter(id=request.user.id)
    user_profile = Profile.objects.get(user=request.user)
    price = Price.objects.get(meal='subscription')
    data = {
        "user": user[0],
        "price": price.price,
        "subscription": user_profile.subscription,
        'orders': history(request)
    }
    return render(request,'profile.html', data)


def logout_view(request):
    logout(request)
    return redirect('/menu/')


def pay(request):
    user = User.objects.get(id=request.user.id)
    user_profile = Profile.objects.get(user=request.user)
    form = Pay(data=request.POST)

    if request.method == 'POST':
        if form.is_valid():
            amount = form.cleaned_data['amount']
            user_profile.balance = user_profile.balance + amount
            user_profile.save()
            return redirect('/user/profile/')
        else:
            return redirect('/user/profile/')

    data = {
        "user": user
    }
    return render(request, 'profile.html', data)


def review(request):
    review_form = ReviewForm(data=request.POST)

    if request.method == 'POST':
        if review_form.is_valid():
            review = Review(user_id=request.user, text=review_form.cleaned_data['text'])
            review.save()
            return redirect('/user/profile/')
        else:
            print("error")
            return redirect('/user/profile/')

    data = {
        "user": request.user
    }
    return render(request, 'profile.html', data)


def subscribe(request):
    user_profile = Profile.objects.get(user=request.user)
    price = Price.objects.get(meal='subscription')
    if user_profile.balance > price.price:
        user_profile.subscription = True
        user_profile.balance = user_profile.balance - price.price
        user_profile.save()

    return redirect('/user/profile/')


def history(request):
    orders = Order.objects.filter(user_id=request.user).order_by('date')[:7]
    return orders