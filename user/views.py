from django.shortcuts import render
from menu.models import *
from django.shortcuts import redirect
from datetime import datetime
from moderator.form import *
from django.contrib.auth.decorators import login_required

today = datetime.now()

months = ['', 'ЯНВ', 'ФЕВ', 'МАР', 'АПР', 'МАЙ']

@login_required(login_url='/login/')
def index(request):
    return redirect(f'/user/{today.year}/{today.month}/{today.day}')


def date(request, year, month, date):
    day = date
    menu = Menu.objects.select_related('dish_id').filter(date=datetime(year, month, day).strftime("%Y-%m-%d"))
    price = Price.objects.all()
    breakfast, dinner, snack = [], [], []

    for m in menu:
        if m.meals == 'breakfast':
            breakfast.append(m.dish_id)
        if m.meals == 'dinner':
            dinner.append(m.dish_id)
        if m.meals == 'snack':
            snack.append(m.dish_id)

    data = {
        'day': day,
        'month': months[month],
        'breakfast': breakfast,
        'dinner': dinner,
        'snack': snack,
        'choose_date': choose_date(year, month, date),
        'price': price,
    }

    if today.strftime("%Y-%m-%d") == datetime(year, month, day).strftime("%Y-%m-%d"):
        data['buy'] = buy_link(request)
    else:
        data['buy'] = {'breakfast': 'Недоступно', 'dinner': 'Недоступно', 'snack': 'Недоступно'}

    return render(request, 'user.html', data)



def buy(request, meal):

    menu = Menu.objects.all().filter(meals=meal, date=today)
    profile = Profile.objects.get(user=request.user)

    if not Order.objects.filter(user_id=request.user, meal_type=meal, date=today).exists():
        order = Order(user_id=request.user, meal_type=meal)

        if profile.subscription == True:
            order.save()
            for m in menu:
                m.count = m.count - 1
                m.save()
        else:
            price = Price.objects.get(meal=meal)
            if profile.balance > price.price:
                profile.balance = profile.balance - price.price
                profile.save()
                order.save()
                for m in menu:
                    m.count = m.count - 1
                    m.save()
            else:
                print('No money')

    return redirect('/user/')


def choose_date(year, month, date):
    text = ""
    days_in_month = (datetime(year, month + 1, 1) - datetime(year, month, 1)).days

    if (date < 15):
        i = 1
        j = days_in_month // 2
    else:
        i = 15
        j = days_in_month

    for number in range(i, j + 1):
        text += f'<a href="/user/{year}/{month}/{number}/">'
        if datetime(year, month, number) == datetime(year, month, date):
            text += (f'<button class ="date_btn bg-primary text-white"><div class ="days text-white">{dow(year, month, number)}</div>{number}</button>')
        elif today.strftime("%Y-%m-%d") == datetime(year, month, number).strftime("%Y-%m-%d"):
            text += f'<button class ="date_btn bg-warning text-white"><div class ="days text-white">{dow(year, month, number)}</div>{number}</button>'
        else:
            text += f'<button class ="date_btn"><div class ="days">{dow(year, month, number)}</div>{number}</button>'
        text += '</a>'

    return text


def dow(year, month, date):
    day_of_week = ['ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ', 'ВС']
    return day_of_week[datetime(year, month, date).weekday()]
def buy_link(request):
    meals = {'breakfast', 'dinner', 'snack'}
    buy = {}
    profile = Profile.objects.get(user=request.user)

    for meal in meals:
        if not Order.objects.filter(user_id=request.user, meal_type=meal, date=today).exists():
            price = Price.objects.get(meal=meal)
            if profile.subscription == True:
                buy[meal] = f'Получить'
            elif profile.balance > price.price:
                buy[meal] = f'Купить'
            else:
                buy[meal] = {}
        else:
            buy[meal] = f'Получен'

    return buy