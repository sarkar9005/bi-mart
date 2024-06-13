from django.contrib import admin
from . models import Product



# Register your models here.

@admin.register(Product)
class Admin(admin.ModelAdmin):
    list_display = ['name', 'desc', 'price', 'img', 'que','subcategory', 'category','id']

    
    