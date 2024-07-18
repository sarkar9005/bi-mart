from django.db import models

# Create your models here.

CATEGORY_CHOICES=(
    ('PN','Paan Corner'),
    ('DBE','Dairy, Braeds & Eggs'),
    ('FV','Fruits & Vegitables'),
    ('CDJ','Cold Drink & juices'),
    ('SM','Snacks & Munchis'),
    ('BFIF','Breakfast & Instant Food'),
    ('ST','Sweet Tooth'),
    ('BB','Bakery & Biscuits'),
    ('TCHD','Tea,Coffe & Health Drink'),
    ('ARD','Atta,Rice & Da'),
    ('MOM','Masala,Oil & More'),
    ('SS','Sauces & Spreads'),
    ('CMF','Chiken,Meat & Fish'),
    ('OHL','Organic & Healthy Living'),
    ('BC','Baby Care'),
    ('pw','Pharma & Wellness'),
    ('CE','Cleaning Essentials'),
    ('HO','Home & Office'),
    ('PC','Personal Care'),
    ('PTC','Pet Care'),
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
    heading = models.ForeignKey(Heading, on_delete=models.PROTECT)
    img = models.ImageField(upload_to='category')

class Subcategory(models.Model):
    id = models.IntegerField(primary_key=True)
    sub_category_code = models.CharField(max_length=255)
    sub_category_name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

class Product(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    desc = models.TextField(null=True, blank=True)
    que = models.TextField(null=True, blank=True)
    price = models.FloatField()
    category = models.ForeignKey(Category, models.PROTECT, null=True, blank=True)
    subcategory = models.ForeignKey(Subcategory, models.PROTECT, null=True, blank=True)
    img = models.ImageField(upload_to='prodcut', null=True, blank=True)

    def __str__(self):
       return self.name

class SpeacialHeadingProduct(models.Model):
    id = models.IntegerField(primary_key=True)
    special_heading = models.ForeignKey(SpecialHeadng, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)