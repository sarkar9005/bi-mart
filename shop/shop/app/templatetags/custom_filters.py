from django import template

register = template.Library()

@register.filter(name='get_item_quantity')
def get_item_quantity(product, cart):
    if not isinstance(cart, dict):
        return False

    product_id_str = str(product.id)
    return product_id_str in cart

@register.filter(name='cart_quantity')
def cart_quantity(product, cart):
    if not isinstance(cart, dict):
        return 0  # Return 0 if cart is not a dictionary

    product_id_str = str(product.id)
    return cart.get(product_id_str, {}).get('quantity', 0)  # Return the quantity if it exists, else 0

@register.filter(name='discounted_price')
def discounted_price(product):
    discounted_price = product.price - (product.price * product.offer_percent / 100) if product.offer_percent else product.price
    return int(discounted_price)  # Remove decimal places

@register.filter(name='total_discounted_price')
def total_discounted_price(item):
    product = item['product']
    quantity = item['quantity']
    price = discounted_price(product)
    return price * quantity

@register.filter(name='final_total')
def final_total(cart_items):
    # Calculate the total discounted price
    total_discounted = sum(
        (item['product'].price - (item['product'].price * item['product'].offer_percent / 100) if item['product'].offer_percent else item['product'].price) * item['quantity']
        for item in cart_items
    )
    
    # Handling charge is always added
    handling_charge = 4
    
    # Delivery charge depends on total discounted price
    delivery_charge = 16 if total_discounted < 200 else 0

    # Return subtotal including handling and delivery charges
    grand_total = total_discounted + handling_charge + delivery_charge
    return int(grand_total)  # Remove decimal places

@register.filter(name='total')
def total(cart_items):
    # Calculate the total discounted price
    total_discounted = sum(
        (item['product'].price - (item['product'].price * item['product'].offer_percent / 100) if item['product'].offer_percent else item['product'].price) * item['quantity']
        for item in cart_items
    )
    return int(total_discounted)  # Remove decimal places

@register.filter(name='actual_total')
def actual_total(cart_items):
    # Calculate the total price without discounts
    total_actual = sum(
        item['product'].price * item['quantity']
        for item in cart_items
    )
    return int(total_actual)  # Remove decimal places

@register.filter
def multiply_no_decimal(value, arg):
    result = value * arg
    return int(result) if result.is_integer() else int(result)  # Remove decimal places
