def cart_count(request):
    if request.user.is_authenticated:
        from .models import Cart
        try:
            cart = Cart.objects.filter(user=request.user).first()
            if cart:
                return {'cart_count': cart.get_total_items()}
        except Cart.DoesNotExist:
            return {'cart_count': 0}
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error getting cart count for user {request.user.id}: {str(e)}")
            return {'cart_count': 0}
    return {'cart_count': 0}