from django.shortcuts import render
from .models import Menu, Dish
from django.shortcuts import redirect
from datetime import datetime


today = datetime.now()


def index(request):
    return redirect(f'/menu/{today.year}/{today.month}/{today.day}')


def date(request, year, month, date):
    day = date
    menu = Menu.objects.select_related('dish_id').filter(date=datetime(year, month, day).strftime("%Y-%m-%d"))
    breakfast, dinner, snack = [], [], []

    # TODO: Нужна сортировка по типам блюд (первое, второе и т.д.)

    for m in menu:
        if m.meals == 'breakfast':
            breakfast.append(m.dish_id)
        if m.meals == 'dinner':
            dinner.append(m.dish_id)
        if m.meals == 'snack':
            snack.append(m.dish_id)

    data = {
        'day': day,
        'month': today.month,
        'breakfast': breakfast,
        'dinner': dinner,
        'snack': snack,
        'choose_date': choose_date(year, month, date)
    }
    return render(request, 'main.html', data)


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
        text += f'<a href="/menu/{year}/{month}/{number}/">'
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

