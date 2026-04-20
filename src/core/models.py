from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=256)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(
        'auth.User', on_delete=models.CASCADE, related_name='orders'
    )
    products = models.ManyToManyField(Product)
    created_at = models.DateTimeField(auto_now_add=True)
