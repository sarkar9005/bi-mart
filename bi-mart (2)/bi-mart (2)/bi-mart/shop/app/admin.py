from django.contrib import admin
from . models import Product
from . models import Subcategory
from . models import Category




# Register your models here.

@admin.register(Product)
class Admin(admin.ModelAdmin):
    list_display = ['name', 'desc', 'price', 'img', 'que','id']

@admin.register(Subcategory)
class Admin(admin.ModelAdmin):
    list_display = ['sub_category_name']

@admin.register(Category)
class Admin(admin.ModelAdmin): 
    list_display = ['category_name']
    