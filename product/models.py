
from django.db import models
from django.contrib.auth.models import User
import random

class ConfirmationCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='confirmation_code')
    code = models.CharField(max_length=6, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = ''.join(str(random.randint(0, 9)) for _ in range(6))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.code}"

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.title

class Review(models.Model):
    text = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    stars = models.IntegerField(default=5)

    def __str__(self):
        return f'Review for {self.product.title}'
