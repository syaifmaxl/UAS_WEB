from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

class FeaturedProduct(models.Model):
    product_name = models.CharField(max_length=300)
    product_img = models.ImageField(upload_to='product_pic')
    price = models.DecimalField(max_digits=10, decimal_places=3)
    def __str__(self):
        return self.product_name


class S_product(models.Model):
    product_name = models.CharField(max_length=300)
    product_img = models.ImageField(upload_to='product_pic')
    price = models.DecimalField(max_digits=10, decimal_places=3)
    description = models.TextField()
    def __str__(self):
        return self.product_name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey('S_product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.product_name} - {self.quantity}"

    def total_price(self):
        return float(self.product.price * self.quantity) 

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(S_product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.product_name} - {self.quantity}"

    def get_total_price(self):
        return self.product.price * self.quantity        

class Product_category(models.Model):
    category_name = models.CharField(max_length=100)
    category_img = models.ImageField(upload_to='category_images/')
    product_total = models.IntegerField(default=0)

    def __str__(self):
        return self.category_name