from django.db import models
from django.contrib.auth.models import User
from products.models import Product


class Cart(models.Model):
    # one cart per user
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        # same product not duplicated
        # clean scaling for checkout system later
        unique_together = ('cart', 'product')