from django.shortcuts import render, get_object_or_404, redirect
from menu.models import Menu, Dish, ChefOrder
from django.shortcuts import redirect
from .form import *
import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test


def role_check(user):
    return user.is_staff

today = datetime.datetime.now()

links = {
    "home": {
        "name": "Общая информация",
        "href": "/moderator/",
    },
    "dish": {
        "name": "Наименование",
        "href": "/moderator/dish/",
    },
    "breakfast": {
        "name": "Завтраки",
        "href": "/moderator/filter/dish/meals/breakfast/",
    },
    "dinner": {
        "name": "Обеды",
        "href": "/moderator/filter/dish/meals/dinner/",
    },
    "snack": {
        "name": "Полдники",
        "href": "/moderator/filter/dish/meals/snack/",
    },
    "add_dish": {
        "name": "Добавить наименование",
        "href": "/moderator/add/dish/",
    },
    "menu": {
        "name": "Меню",
        "href": "/moderator/menu/",
    },
    "add_menu": {
        "name": "Добавить меню",
        "href": "/moderator/add/menu/",
    },
    "orders": {
        "name": "Продажи",
        "href": "/moderator/orders/",
    },

    "chef_order": {
        "name": "Заказы продуктов",
        "href": "/moderator/chef_order/",
    },

    "logout": {
        "name": "Выход",
        "href": "/logout/",
    },
}

months = ['', 'ЯНВ', 'ФЕВ', 'МАР', 'АПР','МАЙ']

MEAL_CHOICES = {
    'breakfast': 'Завтрак',
    'dinner': 'Обед',
    'snack': 'Полдник',
    'all': 'Всегда'
}

def getCalendar(year, month):
    text = ""
    for m in range(len(months)):
        text += f'<a href="/moderator/menu/get_by_date/{year}/{m}/" class="link-light" style="text-decoration: none">{months[m]}</a> '

    text += '<table class="table table-dark">'
    text += "<tr>"
    days = (datetime.date(year, month + 1, 1) - datetime.date(year, month, 1)).days
    for day in range(1, days + 1):
        if day < 10:
            d = f'0{day}'
        else:
            d = day
        text += f'<td><a href="/moderator/menu/get_by_date/{year}/{month}/{d}" class="link-light" style="text-decoration: none">{d}</a></td>'
        if day % 7 == 0:
            text += "</tr><tr>"
    text += "</table>"
    return text


data = {
    "welcome": "Администратор",
    "links": links,
    "calendar": getCalendar(today.year, today.month),
    "meal_choice": MEAL_CHOICES,
    'current_date': datetime.datetime.now(),
}


def navigation():
    nav = []
    for x, obj in links.items():
        for y in obj:
            nav.append(obj)
    data['nav'] = nav


def make_title(request):
    data["title"] = links[request].name


@login_required(login_url='/login/')
def index(request):
    if request.user.profile.role == 'moderator':
        data["title"] = links['home'].get('name')
        data['menu'] = Menu.objects.select_related('dish_id').filter(date=today.strftime("%Y-%m-%d")).order_by('-date')[:10]
        data['orders'] = Order.objects.all().order_by('-date')[:10]
        data['reviews'] = Review.objects.all().order_by('-date')[:10]
        data['chef_orders'] = ChefOrder.objects.all().order_by('-datetime')[:10]
        return render(request, 'moderator_main.html', data)
    else:
        return redirect('/logout/')

@login_required(login_url='/login/')
def menu(request):
    data["title"] = links['menu'].get('name')
    menu = Menu.objects.select_related('dish_id').all().order_by('-date')
    data["menu"] = menu
    return render(request, 'daily_menu.html', data)


@login_required(login_url='/login/')
def dish(request):
    data["title"] = links['dish'].get('name')
    menu = Dish.objects.all().order_by('-id')
    data["menu"] = menu
    return render(request, 'dish.html', data)


@login_required(login_url='/login/')
def order_by(request, table, order_by):
    menu, template = "", ""

    if table == 'menu':
        menu = Menu.objects.select_related('dish_id').all().order_by(f'{order_by}')
        template = 'daily_menu.html'
    if table == 'dish':
        menu = Dish.objects.all().order_by(f'{order_by}')
        template = 'dish.html'

    data["menu"] = menu
    return render(request, template, data)


@login_required(login_url='/login/')
def get_manu_by_date(request, year, month, day=False):
    if day == False:
        day = '01'
    data['calendar'] = getCalendar(year, month)
    date = f'{year}-{month}-{day}'
    data["title"] = f'{day}-{months[month]}-{year}'
    data["menu"] = Menu.objects.select_related('dish_id').all().filter(date=date)
    return render(request, 'daily_menu.html', data)


@login_required(login_url='/login/')
def filtered_by(request, table, row, name):
    menu, template = "", ""
    date = ""

    data["title"] = links[name].get('name')

    if table == 'menu':
        if row == 'breakfast':
            menu = Menu.objects.select_related('dish_id').all().filter(meals=f'{name}')
        if row == 'date':
            menu = Menu.objects.select_related('dish_id').all().filter(date=f'{name}')
            data["title"] = name
        template = 'daily_menu.html'
    if table == 'dish':
        if row == 'meals':
            menu = Dish.objects.all().filter(meals=f'{name}')
        if row == 'type':
            menu = Dish.objects.all().filter(type=f'{name}')
        template = 'dish.html'

    data["menu"] = menu
    return render(request, template, data)

@login_required(login_url='/login/')
def add(request, table):
    if table == 'dish':
        form = DishAddForm(data=request.POST)
    if table == 'menu':
        form = MenuAddForm(data=request.POST)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('/moderator/' + table)
    else:
        if table == 'dish':
            form = DishAddForm()
        if table == 'menu':
            form = MenuAddForm()

    data['form'] = form
    data["title"] = links['add_' + table].get('name')
    return render(request, 'add.html', data)


@login_required(login_url='/login/')
def change(request, table, id):
    if table == 'dish':
        dish = Dish.objects.get(id=id)
        form = DishEditForm(data=request.POST, instance=dish)
    if table == 'menu':
        form = MenuAddForm(data=request.POST)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('/moderator/' + table)
    else:
        if table == 'dish':
            form = DishAddForm({"name": dish.name, "type": dish.type, "meals": dish.meals, "ingredients": dish.ingredients})
        if table == 'menu':
            form = MenuAddForm()

    data['form'] = form
    return render(request, 'change.html', data)

@login_required(login_url='/login/')
def delete(request, table, id):
    if table == 'menu':
        Menu.objects.filter(id=id).delete()
    if table == 'dish':
        Dish.objects.filter(id=id).delete()

    return redirect('/moderator/' + table)


@login_required(login_url='/login/')
def orders(request):
    data["title"] = links['orders'].get('name')
    orders = Order.objects.all()
    data['orders'] = orders
    return render(request, 'orders.html', data)


@login_required(login_url='/login/')
def chef_order(request):
    data["title"] = links['chef_order'].get('name')
    orders = ChefOrder.objects.all().order_by('-datetime')
    data['orders'] = orders
    return render(request, 'chef_order_list.html', data)

@login_required(login_url='/login/')
def chef_order_confirm(request, id):
    ChefOrder.objects.filter(id=id).update(confirmation=True)
    return redirect('/moderator/chef_order/')


@login_required(login_url='/login/')
def chef_order_cancel(request, id):
    ChefOrder.objects.filter(id=id).update(confirmation=False)
    return redirect('/moderator/chef_order/')