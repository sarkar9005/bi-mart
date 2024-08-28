from django.shortcuts import render, get_object_or_404, redirect
import random
# from twilio.rest import Client
from django.conf import settings
from django.utils import timezone
from django.core.mail import send_mail
import razorpay
import json
from django.views import View
from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView
from .models import Product, Heading, Category, SpeacialHeadingProduct, SpecialHeadng, Subcategory, Brand, Customer, Cart, Order, UserAddressBook, PincodeAvailable, OrderProduct
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.http import JsonResponse
from .models import Product, Heading, Category, SpecialHeadng, Subcategory, Brand, Customer, Cart, Order, IdOtp
import string
import random
from .send_mail import send_email

class Home(View):

    def generate_otp(self, number_of_digits):
        otp = ''.join(random.choice(string.digits) for _ in range(number_of_digits))
        return otp
    
    def get(self, request):
        headings = Heading.objects.all()
        special_heading_list = SpecialHeadng.objects.all()
        heading_category_map = {}
        special_heading_product_list = []
        category_subcategory_map = {}

        for heading in headings:
            categories = Category.objects.filter(heading=heading)
            heading_category_map[heading.heading_name] = categories
            for category in categories:
                subcategories = Subcategory.objects.filter(category=category)
                category_subcategory_map[category.category_name] = subcategories

        for special_heading in special_heading_list:
            product_list = []
            for special_product in SpeacialHeadingProduct.objects.filter(special_heading=special_heading.pk):
                product_list.append(special_product.product)
            special_heading_product_list.append({
                "name": special_heading.name,
                "description": special_heading.description,
                "product_list": product_list
            })

        products = Product.objects.all()
        categories = Category.objects.all()

        cart = request.session.get('cart', {})
        if not cart:
            request.session['cart'] = {}

        cart_items = []
        total_price = 0.0
        for item_id, item_data in cart.items():
            product = get_object_or_404(Product, pk=item_id)
            quantity = item_data.get('quantity', 0)
            price = item_data.get('price', 0)
            total_price += quantity * price
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'price': price,
                'subtotal': quantity * price
            })

        total_count = sum(item['quantity'] for item in cart.values())

        context = {
            'heading_category_map': heading_category_map,
            'special_heading_product_list': special_heading_product_list,
            'category_subcategory_map': category_subcategory_map,
            'products': products,
            'categories': categories,
            'cart': cart,
            'cart_items': cart_items,
            'total_price': total_price,
            'total_count': total_count,
        }

        return render(request, 'app/home.html', context)

    def post(self, request):
        product_id = request.POST.get('product_id')
        if product_id:
            return self.handle_add_to_cart(request)

        postData = request.POST
        phone = postData.get('phone')
        email = postData.get('email')
        if phone and len(phone) == 10 and phone.isdigit() and email:
            
            id = ''.join(random.choices(string.ascii_lowercase +
                             string.digits, k=10))
            otp = self.generate_otp(6)
            otpinstance = IdOtp(id = id, otp = otp, phone=phone)
            otpinstance.save()
            send_email(email, otp)
            context = {
                'id' : id,
                'phone' : phone
            }
            return render(request, 'app/profile.html', context)
        else:
            return HttpResponse("Phone number must be exactly 10 digits and numeric.")

    def handle_add_to_cart(self, request):
        product_id = request.POST.get('product_id')
        remove = request.POST.get('remove')
        quantity = int(request.POST.get('quantity', 1))
        mobile_number = request.session.get('mobile_number')
        redirect_url = request.POST.get('redirect_url', '/') 
        if not product_id:
            return JsonResponse({'error': product_id}, status=400)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product does not exist'}, status=404)
        
        
        if mobile_number and product_id:
            cart = request.session.get('cart', {})

            cart_item = cart[str(product_id)]
            
            if remove:
                cart_item['quantity'] -= quantity
                if cart_item['quantity'] <= 0:
                    cart.pop(str(product_id))
                else:
                    cart[str(product_id)] = cart_item
            else:
                cart_item['quantity'] += quantity
                cart[str(product_id)] = cart_item
        else:
            if not remove:
                cart[str(product_id)] = {
                    'quantity': quantity,
                    'price': float(product.price)
                }

        # Update the cart in the session
            request.session['cart'] = cart
       
            total_count = sum(item['quantity'] for item in cart.values())

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'total_count': total_count, 'quantity': cart_item.quantity if cart_item else 0})
            else:
                return redirect(redirect_url)

        return redirect(redirect_url)

    
def logout(request):
    request.session.clear()
    return redirect('home')

class CategoryView(View):
    def get(self, request, val):
        category = get_object_or_404(Category, pk=val)
        subcategories = Subcategory.objects.filter(category=category)
        products = Product.objects.filter(category=category)
        for product in products:
            if product.units:
                product.unit_list = product.units.split(',')
        context = {
            'category': category,
            'subcategories': subcategories,
            'products': products,
        }
        return render(request, "app/category.html", context)

class SubcategoryView(View):
    def get(self, request, val):
        # Get the subcategory and category
        subcategory = get_object_or_404(Subcategory, pk=val)
        category = subcategory.category
        
        # Get the selected brand from the GET request
        brand_filter = request.GET.get('brand', None)
        
        # Filter products by subcategory and brand (if brand is selected)
        if brand_filter:
            products = Product.objects.filter(subcategory=subcategory, brand__name=brand_filter)
        else:
            products = Product.objects.filter(subcategory=subcategory)
        
        # Filter brands associated with the products in this subcategory
        brands = Brand.objects.filter(product__subcategory=subcategory).distinct()
        
        # Prepare the context for the template
        context = {
            'subcategory': subcategory,
            'category': category,
            'subcategories': Subcategory.objects.filter(category=category),
            'products': products,
            'brands': brands,
            'brand_filter': brand_filter,
        }
        
        return render(request, "app/subcategory.html", context)

class ProductDetailView(View):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)

        # Fetch brands associated with the product's category
        brands = Brand.objects.filter(product__category=product.category).distinct()
        
        # Fetch similar products
        similar_products = Product.objects.filter(category=product.category).exclude(pk=product.pk)[:10]
        
        context = {
            'product': product,
            'brands': brands,
            'similar_products': similar_products  
        }
        return render(request, "app/product_detail.html", context)



class BrandDetailView(View):
    def get(self, request, brand_id):
        brand = get_object_or_404(Brand, id=brand_id)
        products = Product.objects.filter(brand=brand)
        return render(request, 'app/brand_detail.html', {'brand': brand, 'products': products})

class MobileProductDetailView(View):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)

        # Fetch brands associated with the product's category
        brands = Brand.objects.filter(product__category=product.category).distinct()
        
        # Fetch similar products
        similar_products = Product.objects.filter(category=product.category).exclude(pk=product.pk)[:10]
        
        context = {
            'product': product,
            'brands': brands,
            'similar_products': similar_products  
        }
        return render(request, "app/product_detail.html", context)

class AllCategoriesView(View):
    def get(self, request):
        categories = Category.objects.prefetch_related('subcategory_set').all()
        selected_category = None
        subcategories = []
        products = []

        if categories:
            selected_category_id = request.GET.get('category_id')
            if selected_category_id:
                selected_category = get_object_or_404(Category, pk=selected_category_id)
            else:
                selected_category = categories.first()

            subcategories = Subcategory.objects.filter(category=selected_category)
            products = Product.objects.filter(category=selected_category)

        context = {
            'categories': categories,
            'selected_category': selected_category,
            'subcategories': subcategories,
            'products': products,
        }
        return render(request, "app/all_categories.html", context)



class AddToCartView(View):
    def post(self, request):
        data = json.loads(request.body)
        product_id = data.get('product_id')
        remove = data.get('remove')
        quantity = int(data.get('quantity'))
        redirect_url = request.POST.get('redirect_url', f"/#product-{product_id}")
        mobile_number = request.session['mobile_number']
        qty = 0
        stock =0 
                    
        # If product_id is not provided, return an error response
        if not product_id:
            return JsonResponse({'error': "product ID is required"}, status=400)
            try:
                product = Product.objects.get(id=product_id)
                
            except Product.DoesNotExist:
                return JsonResponse({'error': 'Product does not exist'}, status=404)

        # Get the current cart from the session
        cart = request.session.get('cart', {})
        product1 = Product.objects.get(id=product_id)    
    

        # Add or update the product in the cart
        if str(product_id) in cart:
            cart_item = cart[str(product_id)]
            cart_item['stock'] = int(product1.stock) 
            stock = int(product1.stock)    
            if remove:
                cart_item['quantity'] -= 1
                qty = cart_item['quantity']
                if cart_item['quantity'] <= 0:
                    cart.pop(str(product_id))
                else:
                    cart[str(product_id)] = cart_item
            else:
                newqty  = cart_item['quantity'] + 1
                if int(product1.stock) >= newqty:
                    cart_item['quantity'] += 1 
                    qty = cart_item['quantity']
                    cart[str(product_id)] = cart_item
                else:
                    cart_item['quantity'] = int(product1.stock) 
                    qty = cart_item['quantity']
                    cart[str(product_id)] = cart_item
                    return JsonResponse({'error': 'Product Stock Not Available',"error_status":"true"})   
                
        else:
            if not remove:
                if int(product1.stock) > 0:
                    cart[str(product_id)] = {
                        'quantity': 1,
                        'price': float(product1.price),
                      #  'discount_price': float(product1.discount_amount),
                        'stock': int(product1.stock)
                    }
                    qty = 1
                    stock = int(product1.stock)
                else:
                    return JsonResponse({'error': 'Product Stock Not Available',"error_status":"true"})

            # Update the cart in the session
        request.session['cart'] = cart
        

        # Calculate the total count of items in the cart
        total_count =0;
        total_sum =0;
    
        for item in cart:
            itemval = cart[item] 
            pricec = itemval.get("price")
            qtyval = itemval.get("quantity")
            total_count = total_count + qtyval
            total_sum = total_sum + (qtyval * pricec) 
        
        # Return a JSON response for AJAX requests or redirect for normal requests
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'total_count': total_count,'totalsum':total_sum, 'quantity': cart.get(str(product_id), {}).get('quantity', 0),'stock':stock,"error_status":"false"})
        else:
            return redirect(redirect_url)




class CartDetailView(View):
    def get(self, request):
        cart_items = []
        total_price = 0.0

        cart = request.session.get('cart', {})
        for item_id, item_data in cart.items():
            product = get_object_or_404(Product, pk=item_id)
            quantity = item_data.get('quantity', 0)
            price = item_data.get('price', 0)
            total_price += quantity * price
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'price': price,
                'subtotal': quantity * price
            })

        context = {
            'cart_items': cart_items,
            'total_price': total_price
        }

        return render(request, 'app/cart.html', context)




class CheckoutFormView(View):
    def get(self, request):
       return render(request, 'app/checkout_form.html', {"is_available" : None})
    
    def post(self, request):
        is_pincode_check = request.POST.get("pincheck")
        if is_pincode_check:
            pincode = request.POST.get('pincode')
            is_pincode_available = PincodeAvailable.objects.filter(pincode=pincode)
            if is_pincode_available:
                context = {
                    "is_available" : 1
                }
            else:
                context = {
                    "is_available" : 0
                }
        
        return render(request, 'app/checkout_form.html', context)
    

class CheckPincodeView(View):
    def post(self, request):
        pincode = request.POST.get('pincode')
        is_pincode_available = PincodeAvailable.objects.filter(pincode=pincode)
        if is_pincode_available:
            context = {
                "is_available" : 1
            }
        else:
            context = {
                "is_available" : 0
            }
        
        return render(request, 'app/checkout_form.html', context)


class CheckoutView(View):
    def post(self, request):
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        name = request.POST.get('name')
        mobile_number = request.session.get('mobile_number')
        cart = request.session.get('cart', {})

        customers = Customer.objects.filter(phone=mobile_number)
        
        if customers.exists():
            customer = customers.first()
        else:
            return HttpResponse("Customer does not exist. Please register.")
        
        order = Order.objects.create(
            customer=customer,
            address=address,
            phone=phone,
            name=name
        )

        total_price_cart = 0
        for product_id, item_data in cart.items():
            product = Product.objects.get(id=product_id)
            quantity = item_data.get('quantity')
            discounted_price = product.price - (product.price * product.offer_percent / 100) if product.offer_percent else product.price

            OrderProduct.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                discounted_price=discounted_price,  # Set the discounted price
                total_price=discounted_price * quantity,  # Calculate the total price
            )

            total_price_cart += discounted_price * quantity

            # Set the product quantity to zero after creating the order
            product.quantity = 0
            product.save()
            print(f"Updated product {product.id} quantity to {product.quantity}")

        # Clear the cart after order is placed
        request.session['cart'] = {}

        # Add handling charge based on the total price
        if total_price_cart > 200:
            total_price_cart += 16
        else:
            total_price_cart += 4

        # Update the total price in the order
        order.total_price = total_price_cart
        order.save()

        # Convert total price to paise and ensure it's an integer
        amount_in_paise = int(total_price_cart * 100)

        client = razorpay.Client(auth=(settings.RAZ_KEY_ID, settings.RAZ_SECRET_KEY))
        payment = client.order.create({'amount': amount_in_paise, 'currency': 'INR', 'payment_capture': 1})
        order.razorpay_order_id = payment.get('id')
        order.save()

        print("-----", payment)

        context = {
            'customer': customer,
            'address': address,
            'phone': phone,
            'name': name,
            'discounted_price': total_price_cart,
            'payment': payment,
            'total_count': 0  # Set total count to 0
        }

        return render(request, 'app/check_out.html', context)

class ProfileView(View):
    def get(self, request):
        mobile_number = request.session.get('mobile_number')
        customer = None
        if mobile_number:
            customer = Customer.objects.filter(phone=mobile_number).first()
        
        context = {
            'customer': customer,
        }
        return render(request, 'app/profile.html', context)

    def post(self, request):
        mobile_number = request.session.get('mobile_number')
        customer = Customer.objects.filter(phone=mobile_number).first()
        if customer:
            latitude = request.POST.get('latitude')
            longitude = request.POST.get('longitude')
            if latitude and longitude:
                customer.latitude = latitude
                customer.longitude = longitude
                customer.save()
                return redirect('profile')
            else:
                return HttpResponse('Latitude and longitude are required.')
        else:
            return HttpResponse('Customer not found.')

def my_addressbook(request):
    return render(request, 'app/my_addressbook.html')


class SearchView(View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q', '')
        if query:
            if 'search_history' not in request.session:
                request.session['search_history'] = []
            if query not in request.session['search_history']:
                request.session['search_history'].append(query)
                request.session.modified = True
            products = Product.objects.filter(name__icontains=query)
        else:
            products = None

        context = {
            'query': query,
            'products': products,
            'search_history': request.session.get('search_history', [])
        }
        return render(request, 'app/search.html', context)

def search_suggestions(request):
    query = request.GET.get('q', '')
    if query:
        suggestions = Product.objects.filter(name__icontains=query).values_list('name', flat=True)[:10]
        return JsonResponse(list(suggestions), safe=False)
    return JsonResponse([], safe=False)

class ClearSearchHistoryView(View):
    def get(self, request):
        request.session['search_history'] = []
        return redirect('search')

class OrderView(View):
    def get(self, request):
        mobile_number = request.session.get('mobile_number')
        if not mobile_number:
            return redirect('login')  # Redirect if user is not logged in

        customer = Customer.objects.filter(phone=mobile_number).first()
        if not customer:
            return HttpResponse("Customer not found.")

        orders = Order.get_orders_by_customer(customer.id)

        return render(request, 'app/orders.html', {'orders': orders})



class SendVerificationCodeView(View):
    def get(self, request):
        # Return a form or any other relevant response for GET requests
        return render(request, 'app/send_code.html')

    def post(self, request):
        phone = request.POST.get('phone')
        if not phone or len(phone) != 10 or not phone.isdigit():
            return HttpResponse("Invalid phone number.")

        customer, created = Customer.objects.get_or_create(phone=phone)
        verification_code = ''.join(random.choices('0123456789', k=6))
        customer.set_verification_code(verification_code)

        # Send OTP via Twilio
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=f"Your verification code is {verification_code}",
            from_=settings.TWILIO_PHONE_NUMBER,
            to=phone
        )

        # Render the verify_code.html page
        return render(request, 'app/verify_code.html')

class VerifyCodeView(View):
    def post(self, request):
        phone = request.POST.get('phone')
        code = request.POST.get('code')

        try:
            customer = Customer.objects.get(phone=phone)
        except Customer.DoesNotExist:
            return HttpResponse("Customer not found.")

        if customer.is_verification_code_valid(code):
            request.session['mobile_number'] = phone
            return redirect('home')
        else:
            return HttpResponse("Invalid or expired verification code.")

def brand_cat(request, brand_id):
    brand = get_object_or_404(Brand, id=brand_id)
    products = Product.objects.filter(brand=brand)
    return render(request, 'app/brand_cat.html', {'brand': brand, 'products': products})

class OtpValidate(View):

    def post(self, request):
        phone = request.POST.get('phone')
        id = request.POST.get('id')
        otp = request.POST.get('otp')

        idotpinst = IdOtp.objects.get(id=id)
        
        if idotpinst and idotpinst.otp == int(otp):
            customer = Customer(phone=phone)
            customer.save()
            request.session['mobile_number'] = phone
            return redirect('home')
        else:
            context = {"id":id, "not_val" : True}
            return render(request, "app/profile.html", context)
