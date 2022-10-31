from distutils.command.upload import upload
import email
from email import message
from email.mime import image
from email.policy import default
from random import seed
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=300)
    address = models.CharField(max_length=200)
    joined_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    bio = models.TextField(max_length=300, null=True)
    image = models.ImageField(upload_to="profileimg",
                              default="images/user.jpg")

    def __str__(self):
        return "Profile:" + str(self.id)


class Category(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title


product_colors = (
    ("White", "White"),
    ("Black", "Black"),
    ("Brown", "Brown"),
    ("Red", "Red"),
    ("Pink", "Pink"),
    ("yellow", "yellow"),
    ("Yellow-black", "Yellow-black"),
    ("Black-white", "Black-white"),
    ("Blue-white", "Blue-white"),
    ("Blue", "Blue"),
    ("All-colors", "All-colors"),

)

shoe_size = (
    ("Large", "Large"),
    ("Medium", "Medium"),
    ("small", "small"),
    ("Allsizes", "Allsizes"),

)


class Product (models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products")
    color = models.CharField(max_length=50, choices=product_colors, null=True)
    shoe_size = models.CharField(max_length=50, choices=shoe_size, null=True)
    discount = models.PositiveIntegerField(null=True, default=0)
    marked_price = models.PositiveIntegerField()
    selling_price = models.PositiveIntegerField()
    description = models.TextField(null=True)
    warranty = models.CharField(max_length=200, null=True, blank=True)
    view_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title


class Cart(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, blank=True)
    total = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Cart:" + str(self.id)


class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rate = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField()

    def __str__(self):
        return "Cart:" + str(self.cart.id) + "CartProduct:" + str(self.id)


ORDER_STATUS = (
    ("Order Received", "Order Received"),
    ("Order Processing", "Order Processing"),
    ("On the way", "On the way"),
    ("Order Canceled", "Order Canceled"),
)


class Order(models.Model):
    cart = models. OneToOneField(Cart, on_delete=models.CASCADE)
    ordered_by = models.CharField(max_length=200)
    shipping_address = models.CharField(max_length=200)
    mobile = models.CharField(max_length=10)
    email = models.EmailField(null=True, blank=True)
    subtotal = models.PositiveIntegerField()
    total = models.PositiveIntegerField()
    order_status = models.CharField(max_length=50, choices=ORDER_STATUS)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Order:" + str(self.id)


class Contact (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Phone_number = models.PositiveBigIntegerField(default=0)
    subject = models.CharField(max_length=200, null=True, blank=True)
    message = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return "Contact:" + str(self.id)
