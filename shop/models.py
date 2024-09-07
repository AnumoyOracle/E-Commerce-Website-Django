from django.db import models
from datetime import datetime

# Create your models here. 


class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=100)
    category = models.CharField(max_length=200, default="")
    subcategory = models.CharField(max_length=200, default="")
    price = models.IntegerField(default=0)
    product_desc = models.TextField()
    pub_date = models.DateField()
    image = models.ImageField(upload_to="shop/img", default="")

    def __str__(self):
        return self.product_name


class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=200, default="john.doe@gmail.com")
    phone = models.CharField(max_length=20)
    desc = models.CharField(max_length=1000)

    def __str__(self):
        return self.name


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    items_json = models.CharField(max_length=10000)
    name = models.CharField(max_length=90)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    amount = models.IntegerField(default=0)
    rzp_order_id = models.CharField(max_length=200, default="")
    rzp_payment_id = models.CharField(max_length=200, default="")
    payment_status = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class OrderUpdate(models.Model):
    update_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default=0)
    update_desc = models.CharField(max_length=5000)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.update_desc[0:7] + "..."
