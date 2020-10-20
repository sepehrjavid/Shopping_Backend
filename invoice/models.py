from django.contrib.auth.models import User
from django.db import models

from products.models import Cloth

SHOPPING = "Shopping"
PENDING = "Pending"
DELIVERING = "Delivering"
DELIVERED = "Delivered"


class Order(models.Model):
    STATES = (
        ("Shopping", "Shopping"),
        ("Pending", "Pending"),
        ("Delivering", "Delivering"),
        ("Delivered", "Delivered"),
    )
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='orders')
    date = models.DateTimeField(auto_now_add=True)
    state = models.CharField(max_length=10, default="Shopping", choices=STATES)

    def __str__(self):
        return self.user.username + " | " + str(self.date) + " | " + self.state


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('products.Product', on_delete=models.PROTECT)
    count = models.IntegerField(default=1)
    price = models.FloatField()
    size = models.ForeignKey('products.Size', on_delete=models.PROTECT, null=True)
    color = models.ForeignKey('products.Color', on_delete=models.PROTECT, null=True)

    def __str__(self):
        self.order.user.username + " | " + str(self.order.date) + " | " + self.order.state + " | " + self.product.title
