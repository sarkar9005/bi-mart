from django.contrib import admin
from .models import Product, Heading, Category, Subcategory, SpeacialHeadingProduct, SpecialHeadng, Brand, Customer, Cart, Order, UserAddressBook, PincodeAvailable, OrderProduct, IdOtp

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'id', 'desc', 'detail_1', 'detail_2', 'detail_3', 'detail_4', 'detail_5', 'detail_6', 'detail_7', 'detail_8', 'detail_9', 'detail_10', 'detail_11', 'detail_12', 'detail_13', 'detail_14', 'detail_15', 'detail_16', 'detail_17', 'detail_18', 'detail_19', 'detail_20', 'detail_21', 'detail_22', 'detail_23', 'detail_24', 'detail_25', 'detail_26', 'detail_27', 'detail_28', 'detail_29', 'detail_30',  'price', 'offer_percent', 'image1', 'image2', 'image3', 'image4', 'image5', 'que', 'subcategory']

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




class OrderAdmin(admin.ModelAdmin):
    list_display = ('address', 'phone', 'name', 'time', 'date', 'order_status', 'paid_status')

    def discounted_price(self, obj):
        """Calculate and return the discounted price of the product."""
        price = obj.product.price - (obj.product.price * obj.product.offer_percent / 100) if obj.product.offer_percent else obj.product.price
        return int(price)  # Return as integer without decimal places

    def total_discounted_price(self, obj):
        """Calculate and return the total discounted price with delivery and handling charges."""
        discounted_price = self.discounted_price(obj)
        total_price = discounted_price * obj.quantity
        
        # Debugging values
        print(f"Discounted Price: {discounted_price}, Quantity: {obj.quantity}, Total Price: {total_price}")

        # Add handling charge
        handling_charge = 4
        
        # Add delivery charge if total discounted price is less than 200
        delivery_charge = 16 if total_price < 200 else 0
        
        # Final price with handling and delivery charges
        final_price = total_price + handling_charge + delivery_charge

        # Debugging final price
        print(f"Handling Charge: {handling_charge}, Delivery Charge: {delivery_charge}, Final Price: {final_price}")

        return int(final_price)

    discounted_price.short_description = 'Discounted Price'
    total_discounted_price.short_description = 'Total Discounted Price'

admin.site.register(Order, OrderAdmin)

class UserAddressBookAdmin(admin.ModelAdmin):
    list_display = ['user', 'address', 'status']
admin.site.register(UserAddressBook,UserAddressBookAdmin)

@admin.register(PincodeAvailable)
class PincodeAdmin(admin.ModelAdmin):
    list_display = ['pincode']

@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'discounted_price', 'total_price']

@admin.register(IdOtp)
class IdOtpadmin(admin.ModelAdmin):
    pass