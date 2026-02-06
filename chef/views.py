from django.shortcuts import render
import datetime
from menu.models import *
from django.shortcuts import redirect
from moderator.form import *
from django.contrib.auth.decorators import login_required


today = datetime.datetime.now()

links = {
    "home": {
        "name": "Общая информация",
        "href": "/chef/",
    },
    "dish": {
        "name": "Остаток",
        "href": "/chef/list/",
    },

    "orders": {
        "name": "Продажи",
        "href": "/chef/orders/",
    },

    "add": {
        "name": "Заказ продуктов",
        "href": "/chef/add/",
    },

    "chef_order": {
        "name": "Список заказов",
        "href": "/chef/chef_order/",
    },

    "logout": {
        "name": "Выход",
        "href": "/logout/",
    },
}

data = {
    "welcome": "Повар",
    "links": links,
    'current_date': today,
}

@login_required(login_url='/login/')
def index(request):
    if request.user.profile.role == 'chef':
        data["title"] = links['home'].get('name')
        data['menu'] = Menu.objects.select_related('dish_id').filter(date=today.strftime("%Y-%m-%d")).order_by('-date')[:10]
        data['orders'] = Order.objects.all().order_by('-date')[:10]
        data['reviews'] = Review.objects.all().order_by('-date')[:10]
        data['chef_orders'] = ChefOrder.objects.all().order_by('-datetime')[:10]
        return render(request, 'chef_main.html', data)
    else:
        return redirect('/logout/')

@login_required(login_url='/login/')
def list(request):
    data["title"] = links['dish'].get('name')
    menu = Menu.objects.all().order_by('-date')
    data["menu"] = menu
    return render(request, 'list.html', data)


@login_required(login_url='/login/')
def orders(request):
    data["title"] = links['orders'].get('name')
    orders = Order.objects.all()
    data['orders'] = orders
    return render(request, 'chef_orders.html', data)


@login_required(login_url='/login/')
def add_order(request):
    if request.method == 'POST':
        form = ChefOrderForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/chef/')
    else:
        form = ChefOrderForm()

    data['form'] = form
    data["title"] = links['add'].get('name')
    return render(request, 'chef_add.html', data)


@login_required(login_url='/login/')
def chef_order(request):
    data["title"] = links['chef_order'].get('name')
    orders = ChefOrder.objects.all().order_by('-datetime')
    data['orders'] = orders
    return render(request, 'chef_list.html', data)


@login_required(login_url='/login/')
def navigation():
    nav = []
    for x, obj in links.items():
        for y in obj:
            nav.append(obj)
    data['nav'] = nav