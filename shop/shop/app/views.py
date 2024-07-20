from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.http import HttpResponse, JsonResponse
from .models import Product, Heading, Category, SpeacialHeadingProduct, SpecialHeadng, Subcategory, Brand, Customer, Cart, Order, UserAddressBook, PincodeAvailable

class Home(View):
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

        cart = request.session.get('cart')
        if not cart:
            request.session['cart'] = {}

        context = {
            'heading_category_map': heading_category_map,
            'special_heading_product_list': special_heading_product_list,
            'category_subcategory_map': category_subcategory_map,
            'products': products,
            'categories': categories,
            'cart': cart
        }

        return render(request, 'app/home.html', context)

    def post(self, request):
        postData = request.POST
        phone = postData.get('phone')

        if phone and len(phone) == 10 and phone.isdigit():
            customer = Customer(phone=phone)
            customer.save()
            request.session['mobile_number'] = phone
            return redirect('home')
        else:
            return HttpResponse("Phone number must be exactly 10 digits and numeric.")
    
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
        subcategory = get_object_or_404(Subcategory, pk=val)
        category = subcategory.category  
        subcategories = Subcategory.objects.filter(category=category)
        products = Product.objects.filter(subcategory=subcategory)
        brand_filter = request.GET.get('brand', None)
        
        brands = Brand.objects.filter(product__subcategory=subcategory).distinct()
        
        context = {
            'subcategory': subcategory,
            'category': category,
            'subcategories': subcategories,
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
        product_id = request.POST.get('product_id')
        remove = request.POST.get('remove')
        quantity = int(request.POST.get('quantity', 1))
        mobile_number = request.session.get('mobile_number')
        redirect_url = request.POST.get('redirect_url', '/product/{}/'.format(product_id))


        if not product_id:
            return JsonResponse({'error': 'Product ID is required'}, status=400)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product does not exist'}, status=404)

        if mobile_number:
            cart_item, created = Cart.objects.get_or_create(
                mobile_number=mobile_number,
                product=product,
                defaults={'quantity': quantity, 'price': product.price}
            )
            if not created:
                if remove:
                    cart_item.quantity -= quantity
                    if cart_item.quantity <= 0:
                        cart_item.delete()
                        cart_item = None
                    else:
                        cart_item.save()
                else:
                    cart_item.quantity += quantity
                    cart_item.save()

            # Update session cart
            cart = request.session.get('cart', {})
            if cart_item:
                cart[str(product.id)] = {
                    'quantity': cart_item.quantity,
                    'price': float(cart_item.price)
                }
            else:
                cart.pop(str(product.id), None)
            request.session['cart'] = cart

            return redirect(redirect_url)
        
        return JsonResponse({'error': 'Mobile number not found in session'}, status=400)



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
        mobile_number = request.session.get('mobile_number')
        cart = request.session.get('cart', {})

        # Retrieve customer using phone number
        customers = Customer.objects.filter(phone=phone)
        
        if customers.exists():
            customer = customers.first()
        else:
            # Handle case where customer does not exist
            return HttpResponse("Customer does not exist. Please register.")

        print(f"Phone: {phone}, Address: {address}, mobile_number: {mobile_number}")
        print("Cart Items:")
        for product_id, item_data in cart.items():
            product = Product.objects.get(id=product_id)
            quantity = item_data.get('quantity')
            print(f"Product: {product.name}, Quantity: {quantity}")

            # Create Order for each product in cart associated with customer
            order = Order.objects.create(
                customer=customer,
                product=product,
                price=product.price,
                address=address,
                phone=phone,
                quantity=quantity
            )

            # You can perform additional operations with the order here if needed
            order.save()

        # Clear cart after placing order
        request.session['cart'] = {}  # Corrected assignment here

        context = {
            'phone': phone,
            'address': address,
            'mobile_number': mobile_number,
            'cart': cart  # Ensure cart is passed back to context if needed
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
