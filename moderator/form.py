from django import forms
from menu.models import *


class DishAddForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = '__all__'

    MEAL_CHOICES = [
        ('all', 'Всегда'),
        ('breakfast', 'Завтрак'),
        ('dinner', 'Обед'),
        ('snack', 'Полдник'),
    ]
    DISH_TYPE = [
        (0, 'Нет'),
        (1, 'Салат'),
        (2, 'Первое блюдо'),
        (3, 'Второе блюдо'),
        (4, 'Напиток')
    ]
    name = forms.CharField(label="Наименование", max_length=180, widget=forms.TextInput(attrs={"class": "form-control"}))
    type = forms.ChoiceField(label="Категория", choices=DISH_TYPE, widget=forms.Select(attrs={"class": "form-control"}))
    meals = forms.ChoiceField(label="Приём пищи", choices=MEAL_CHOICES, widget=forms.Select(attrs={"class": "form-control"}))
    ingredients= forms.CharField(
        label="Состав",
        widget=forms.Textarea(attrs={"required": False, "class": "form-control"})
    )


class MenuAddForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = '__all__'

    MEAL_CHOICES = [
        ('breakfast', 'Завтрак'),
        ('dinner', 'Обед'),
        ('snack', 'Полдник'),
    ]
    date = forms.DateField(label="Дата", widget=forms.SelectDateWidget(attrs={"class": "form-control"}))
    count = forms.IntegerField(label="Количество", widget=forms.NumberInput(attrs={"class": "form-control"}))
    dish_id = forms.ModelChoiceField(label="Блюдо",queryset=Dish.objects.all(), widget=forms.Select(attrs={"class": "form-control"}))
    meals = forms.ChoiceField(
        label="Приёмы пищи", choices=MEAL_CHOICES, widget=forms.Select(attrs={"class": "form-select"})
    )


class DishEditForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = '__all__'


class ReviewForm(forms.Form):
    class Meta:
        model = Review
        fields = '__all__'

    text = forms.CharField(max_length=255, widget=forms.Textarea)


class Pay(forms.Form):
    amount = forms.IntegerField(label="Сумма", widget=forms.NumberInput(attrs={"class": "form-control"}))


class ChefOrderForm(forms.ModelForm):
    class Meta:
        model = ChefOrder
        fields = ['text']

    text = forms.CharField(label="Необходимые продукты", widget=forms.Textarea(attrs={"class": "form-control"}))


class RegisterForm(forms.Form):
    class Meta:
        model = User
        field = '_all_'

    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(label='Адрес электронной почты', widget=forms.EmailInput(attrs={'class': 'form-control'}))
