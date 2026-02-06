from django.db import models
from django.contrib.auth.models import User


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

ROLE = [
    ('student', 'Ученик'),
    ('chef', 'Повар'),
    ('moderator', 'Модератор')
]


class Dish(models.Model):

    name = models.CharField(max_length=255)
    type = models.IntegerField(
        choices=DISH_TYPE,
        default=0
    )
    meals = models.CharField(
        max_length=20,
        choices=MEAL_CHOICES,
        default='breakfast'
    )
    ingredients = models.CharField(max_length=255)
    picture = models.ImageField(default='/static/img/default.png', upload_to='static/img/')

    def __str__(self):
        return f"{self.name}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.FloatField(default=0.0)
    role = models.CharField(max_length=20, choices=ROLE, default='student')
    subscription = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Menu(models.Model):
    date = models.DateField()
    count = models.IntegerField()
    dish_id = models.ForeignKey(Dish, on_delete=models.CASCADE)
    meals = models.CharField(
        max_length=20,
        choices=MEAL_CHOICES,
        default='breakfast'
    )

    def __str__(self):
        return f"{self.dish_id} {self.date}"


class Order(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    meal_type = models.CharField(default=False, choices=MEAL_CHOICES)

    def __str__(self):
        return f"{self.user_id} {self.date} {self.meal_type}"


class Review(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user_id} | {self.date}"


class Price(models.Model):
    MEAL_CHOICES = [
        ('subscription', 'Абонемент'),
        ('breakfast', 'Завтрак'),
        ('dinner', 'Обед'),
        ('snack', 'Полдник'),
    ]
    meal = models.CharField(max_length=20, choices=MEAL_CHOICES, default='breakfast')
    price = models.FloatField()

    def __str__(self):
        return f"{self.meal} {self.price}"


class ChefOrder(models.Model):
    text = models.CharField(max_length=255)
    datetime = models.DateTimeField(auto_now=True)
    confirmation = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.datetime} {self.confirmation}"
