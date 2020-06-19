from django.db import models
from django.shortcuts import reverse
from django.conf import settings

PRODUCT_CHOICES = (
    ('S', 'Shirt'),
    ('P', 'Pant'),
    ('T', 'T-Shirt')
)


class Item(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to='media', null=True, blank=True)
    description = models.TextField()
    price = models.FloatField()
    label = models.CharField(choices=PRODUCT_CHOICES, max_length=1)
    slug = models.SlugField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('store', kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse('add_to_cart', kwargs={
            'slug': self.slug
        })


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quantity} {self.item.name } of {self.user.first_name} {self.user.last_name}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_count(self):
        return self.quantity


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}'s Orders"

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_total_item_price()
        return total

    def get_total_count(self):
        total_count = 0
        for order_item in self.items.all():
            total_count += order_item.get_total_count()
        return total_count


class UserDetail(models.Model):
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pin_code = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=10)
