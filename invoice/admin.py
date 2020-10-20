from django.contrib import admin

from invoice.models import Order, OrderItem

admin.site.register(Order)
admin.site.register(OrderItem)
