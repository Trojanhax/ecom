from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.name} {self.email}"


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    digital = models.BooleanField(default=False, null=True, blank=True)
    image = models.ImageField(null=True, )

    def __str__(self):
        return f"{self.name} {self.price}"

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except FileNotFoundError:
            url = ''  # Provide a default image URL
        return url


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f"{self.transaction_id} {self.date_ordered}"

    @property
    def shipping(self):
        shipping_required = False  # Renamed variable to avoid conflict
        orderitems = self.orderitem_set.all()
        for order_item in orderitems:
            if not order_item.product.digital:
                shipping_required = True
                break  # Break out of the loop as soon as a non-digital product is found
        return shipping_required

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_item(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.order} {self.quantity}"

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    zipcode = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.order} {self.address}"


class Contact(models.Model):
    msg_id = models.AutoField
    name = models.CharField(max_length=30)
    email = models.CharField(max_length=25, default="")
    phone = models.CharField(max_length=14, default="")
    desc = models.CharField(max_length=500)

    def __str__(self):
        return f" {self.name} {self.email} {self.phone} "
