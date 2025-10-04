def cart_count(request):
    if request.user.is_authenticated:
        from .models import Cart
        try:
            cart = Cart.objects.filter(user=request.user).first()
            if cart:
                return {'cart_count': cart.get_total_items()}
        except:
            pass
    return {'cart_count': 0}