from django.db import models
from djmoney.models.fields import MoneyField

class Project(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('purchased', 'Purchased'),
    )
    name = models.CharField(max_length=100)
    price = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return self.name

class Transaction(models.Model):
    transaction_id = models.CharField(max_length=100, unique=True)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True)
    amount = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')
    invoice_id = models.CharField(max_length=100)
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField()
    raw_data = models.JSONField()  # Store full webhook payload

    def __str__(self):
        return f"{self.transaction_id} - {self.status}"