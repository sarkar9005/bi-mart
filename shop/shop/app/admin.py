from django.contrib import admin
from .models import Product, Heading, Category, Subcategory, SpeacialHeadingProduct, SpecialHeadng, Brand, Customer, Cart, Order, UserAddressBook, PincodeAvailable, OrderProduct

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'id', 'desc',  'price', 'offer_percent', 'image1', 'image2', 'image3', 'image4', 'image5', 'que', 'subcategory']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["category_name"]

@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ['sub_category_name']

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Heading)
class HeadingAdmin(admin.ModelAdmin):
    list_display = ['heading_name']

@admin.register(SpecialHeadng)
class SpecialHeadngAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(SpeacialHeadingProduct)
class SpeacialHeadingProductAdmin(admin.ModelAdmin):
    list_display = ['special_heading', 'id']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['mobile_number', 'product', 'quantity', 'price']

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['phone']

@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'discounted_price', 'total_price']

class OrderAdmin(admin.ModelAdmin):
    list_display = ('address', 'phone', 'name', 'time', 'date', 'order_status', 'paid_status')


admin.site.register(Order, OrderAdmin)

class UserAddressBookAdmin(admin.ModelAdmin):
    list_display = ['user', 'address', 'status']
admin.site.register(UserAddressBook,UserAddressBookAdmin)

@admin.register(PincodeAvailable)
class PincodeAdmin(admin.ModelAdmin):
    list_display = ['pincode']