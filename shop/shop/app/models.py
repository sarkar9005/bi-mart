# models.py
from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
import datetime

CATEGORY_CHOICES = (
    ('PN', 'Paan Corner'),
    ('DBE', 'Dairy, Braeds & Eggs'),
    ('FV', 'Fruits & Vegitables'),
    ('CDJ', 'Cold Drink & juices'),
    ('SM', 'Snacks & Munchis'),
    ('BFIF', 'Breakfast & Instant Food'),
    ('ST', 'Sweet Tooth'),
    ('BB', 'Bakery & Biscuits'),
    ('TCHD', 'Tea,Coffe & Health Drink'),
    ('ARD', 'Atta,Rice & Da'),
    ('MOM', 'Masala,Oil & More'),
    ('SS', 'Sauces & Spreads'),
    ('CMF', 'Chiken,Meat & Fish'),
    ('OHL', 'Organic & Healthy Living'),
    ('BC', 'Baby Care'),
    ('pw', 'Pharma & Wellness'),
    ('CE', 'Cleaning Essentials'),
    ('HO', 'Home & Office'),
    ('PC', 'Personal Care'),
    ('PTC', 'Pet Care'),
)

class SpecialHeadng(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name

class Heading(models.Model):
    id = models.IntegerField(primary_key=True)
    heading_name = models.CharField(max_length=255)

class Category(models.Model):
    id = models.IntegerField(primary_key=True)
    category_code = models.CharField(max_length=255)
    category_name = models.CharField(max_length=255)
    heading = models.ForeignKey(Heading, on_delete=models.PROTECT, null=True, blank=True)
    img = models.ImageField(upload_to='category', null=True, blank=True)

    def __str__(self):
        return self.category_name

class Subcategory(models.Model):
    id = models.IntegerField(primary_key=True)
    sub_category_code = models.CharField(max_length=255)
    sub_category_name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    img = models.ImageField(upload_to='product', null=True, blank=True)

    def __str__(self):
        return self.sub_category_name

class Brand(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='prodcut', null=True, blank=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    desc = models.TextField(null=True, blank=True)
    que = models.TextField(null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    offer_percent = models.IntegerField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True, blank=True)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.PROTECT, null=True, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, null=True, blank=True)
    image1 = models.ImageField(upload_to='prodcut', null=True, blank=True)
    image2 = models.ImageField(upload_to='prodcut', null=True, blank=True)
    image3 = models.ImageField(upload_to='prodcut', null=True, blank=True)
    image4 = models.ImageField(upload_to='prodcut', null=True, blank=True)
    image5 = models.ImageField(upload_to='prodcut', null=True, blank=True)# e.g., "small,large"

    def __str__(self):
        return self.name


    def discounted_price(self):
        if self.offer_percent is not None and self.offer_percent > 0 and self.offer_percent < 100:
            discount_amount = (self.offer_percent / 100) * self.price
            return self.price - discount_amount
        elif self.offer_percent is not None and self.offer_percent >= 100:
            return 0
        else:
            return self.price

class SpeacialHeadingProduct(models.Model):
    id = models.IntegerField(primary_key=True)
    special_heading = models.ForeignKey(SpecialHeadng, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)




class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    phone = models.CharField(max_length=50, null=True, blank=True, unique=True)
    verification_code = models.CharField(max_length=6, null=True, blank=True)
    verification_expiry = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.phone if self.phone else ''

    def register(self):
        self.save()

    def set_verification_code(self, code):
        self.verification_code = code
        self.verification_expiry = timezone.now() + timedelta(minutes=10)
        self.save()

    def is_verification_code_valid(self, code):
        return self.verification_code == code and timezone.now() <= self.verification_expiry




class Cart(models.Model):
    mobile_number = models.CharField(max_length=15, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.mobile_number} - {self.product.name} - {self.quantity}'

status_choice=(
    ('process', 'In Process'),
    ('shipped', 'Shipped'),
    ('deliverd', 'Deliverd'),
)
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    address = models.CharField(max_length=50, null=False, blank=False, default="")
    phone = models.CharField(max_length=10, null=False, blank=False, default="")
    name = models.CharField(max_length=10, null=False, blank=False, default="")
    time = models.TimeField(default=datetime.datetime.today)
    date = models.DateField(default=datetime.datetime.today)
    order_status = models.CharField(max_length=50, choices=status_choice, default='process')
    paid_status = models.BooleanField(default=False)
    razorpay_order_id = models.CharField(max_length=255, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=255, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=255, null=True, blank=True)
    total_price = models.IntegerField(null=True)

    @staticmethod
    def get_orders_by_customer(customer_id):
        return Order.objects.filter(customer_id=customer_id)

    

    

class UserAddressBook(models.Model):
    user=models.ForeignKey(Customer,on_delete=models.CASCADE)
    address=models.TextField()
    status=models.BooleanField(default=False)

class PincodeAvailable(models.Model):
    pincode = models.CharField(max_length=6)

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField(default=1)
    discounted_price = models.IntegerField(null=True)
    total_price = models.IntegerField(null=True)

