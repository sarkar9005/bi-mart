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




@register.filter
def multiply_no_decimal(value, arg):
    result = value * arg
    return int(result) if result.is_integer() else result