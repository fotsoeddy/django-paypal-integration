from django.db import models
from djmoney.models.fields import MoneyField

class Project(models.Model):
    name = models.CharField(max_length=100)
    price = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name