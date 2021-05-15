import datetime

from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify

# Create your models here.
MEALS = (
    ("B", 'Breakfast'),
    ("L", 'Lunch'),
    ('D', 'Dinner'),
    (None, 'Meal')
)
MEAL_NAMES = {'B': 'Breakfast', 'L': 'Lunch', 'D': 'Dinner'}
HALLS = (
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
    (6, '6'),
    (7, '7'),
    (8, '8'),
    (9, '9'),
    (10, '10'),
    (11, '11'),
    (12, '12'),
    (13, '13'),
    (None, 'Hall Number')
)


class Coupon(models.Model):
    meal = models.CharField(choices=MEALS, max_length=1, blank=False)
    hall = models.PositiveSmallIntegerField(choices=HALLS)
    price = models.PositiveSmallIntegerField()
    sold = models.BooleanField(default=False)

    date_published = models.DateTimeField(auto_now_add=True, verbose_name='date published')
    date_updated = models.DateTimeField(auto_now=True, verbose_name='date updated')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.SlugField(blank=True, unique=True)

    def __str__(self):
        return str(self.meal) + ' at Hall-' + str(self.hall)

    @property
    def get_meal_name(self):
        return MEAL_NAMES.get(self.meal)


def pre_save_coupon(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.author.username + '-' + datetime.datetime.now().strftime("%H%M%S%f"))


pre_save.connect(pre_save_coupon, sender=Coupon)
