from django.conf import settings

def cart_count(request):
    cart = request.session.get('cart', {})
    cart_count = sum(item.get('quantity', 1) for item in cart.values())
    return {'cart_count': cart_count}
