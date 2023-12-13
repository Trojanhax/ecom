from django.contrib import admin
from .models import Contact, Customer, Product, ShippingAddress, Order, OrderItem


# Register your models here.
class CustomerAdmin(admin.ModelAdmin):
    # Add configuration for CustomerAdmin if needed
    list_display = ("name", "email",)


class ProductAdmin(admin.ModelAdmin):
    # Add configuration for ProductAdmin if needed
    list_display = ("name", "price",)


class ShippingAddressAdmin(admin.ModelAdmin):
    # Add configuration for ShippingAddressAdmin if needed
    list_display = ("order", "address",)


class OrderAdmin(admin.ModelAdmin):
    # Add configuration for OrderAdmin if needed
    list_display = ("transaction_id", "date_ordered",)


class OrderItemAdmin(admin.ModelAdmin):
    # Add configuration for OrderItemAdmin if needed
    list_display = ("order", "quantity",)


class ContactAdmin(admin.ModelAdmin):
    # Add configuration for ContactAdmin if needed
    list_display = ("name", "email", "phone",)


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ShippingAddress, ShippingAddressAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Contact, ContactAdmin)
