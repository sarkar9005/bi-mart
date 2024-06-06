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

class Product(models.Model):
    name = models.CharField(max_length=100)
    desc = models.TextField()
    que = models.TextField()
    price = models.FloatField()
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=5)
    subcategory = models.CharField( max_length=100)
    img = models.ImageField(upload_to='prodcut')

    def __str__(self):
       return self.name
