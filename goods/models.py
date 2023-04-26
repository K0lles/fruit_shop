from django.db import models


class Goods(models.Model):

    class NameChoices(models.TextChoices):
        pineapple = ('pineapple', 'Ананаси')
        apple = ('apple', 'Яблука')
        banana = ('banana', 'Банани')
        orange = ('orange', 'Апельсини')
        apricot = ('apricot', 'Абрикоси')
        kiwi = ('kiwi', 'Ківі')

    name = models.CharField(max_length=9, choices=NameChoices.choices)
    amount = models.PositiveIntegerField()


class Bank(models.Model):
    account = models.PositiveIntegerField()
