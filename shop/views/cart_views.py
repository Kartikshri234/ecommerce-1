"""Cart & Checkout Views"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse

from shop.models import Product, Cart, CartItem, Order


@login_required
def add_to_cart(request, product_id):
    """Add product to cart via AJAX"""
    if request.method == 'POST':
        try:
            product = get_object_or_404(Product, id=product_id)

            if product.stock <= 0:
                return JsonResponse({
                    'success': False,
                    'message': 'Product is out of stock ❌'
                }, status=400)

            # Get quantity from request
            quantity = request.POST.get('quantity', 1)
            try:
                quantity = int(quantity)
                if quantity < 1:
                    quantity = 1
                elif quantity > product.stock:
                    quantity = product.stock
            except (ValueError, TypeError):
                quantity = 1

            cart, created = Cart.objects.get_or_create(user=request.user)
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                defaults={"quantity": quantity},
            )

            if not created:
                new_quantity = cart_item.quantity + quantity
                if new_quantity > product.stock:
                    new_quantity = product.stock
                    message = f"Stock limit reached for {product.name}"
                else:
                    message = f"Increased {product.name} quantity in cart!"
                cart_item.quantity = new_quantity
                cart_item.save()
            else:
                message = f"{product.name} added to cart!"

            return JsonResponse({
                'success': True,
                'cart_count': cart.get_total_items(),
                'message': message
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error adding to cart: {str(e)}'
            }, status=500)
    
    return JsonResponse({
        'success': False,
        'message': 'Invalid request'
    }, status=400)


@login_required
def cart_view(request):
    """Display shopping cart"""
    cart = Cart.objects.filter(user=request.user).first()
    cart_items = cart.items.select_related('product').all() if cart else []
    total = sum(item.get_total() for item in cart_items)
    return render(request, 'cart.html', {
        'cart': cart,
        'cart_items': cart_items,
        'total': total,
    })


@login_required
def update_cart(request, item_id):
    """Update cart item quantity"""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

    action = request.POST.get("action")
    if action == "increase" and cart_item.quantity < cart_item.product.stock:
        cart_item.quantity += 1
        cart_item.save()
    elif action == "decrease":
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()

    return redirect("cart")


@login_required
def remove_from_cart(request, item_id):
    """Remove item from cart"""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    messages.info(request, "Item removed from cart.")
    return redirect("cart")


@login_required
def checkout(request):
    """Checkout view - process order"""
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    if not cart_items.exists():
        messages.warning(request, "Your cart is empty!")
        return redirect("product_list")

    total = sum(item.get_total() for item in cart_items)

    if request.method == "POST":
        payment_method = request.POST.get("payment_method", "").strip()
        full_name = request.POST.get("full_name", "").strip()
        phone = request.POST.get("phone", "").strip()
        address = request.POST.get("address_line1", "").strip()
        city = request.POST.get("city", "").strip()
        
        # Validate required fields
        if not all([payment_method, full_name, phone, address, city]):
            messages.error(request, "Please fill in all required fields.")
            return render(request, "checkout.html", {
                "cart_items": cart_items,
                "total": total,
            })
        
        # Validate payment method
        if payment_method not in ['cod', 'razorpay']:
            messages.error(request, "Invalid payment method selected.")
            return render(request, "checkout.html", {
                "cart_items": cart_items,
                "total": total,
            })

        # Create order
        order = Order.objects.create(
            user=request.user,
            total_amount=total,
            payment_method=payment_method,
            shipping_address=f"{full_name}, {phone}, {address}, {city}",
        )

        # Move cart items into order
        for item in cart_items:
            order.items.create(
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
            )
            # Reduce stock
            item.product.stock -= item.quantity
            item.product.save()

        # Clear cart
        cart_items.delete()

        # Redirect to Razorpay if payment method is Razorpay
        if payment_method == 'razorpay':
            return redirect('razorpay_checkout', order_id=order.id)
        else:
            messages.success(request, "Order placed successfully! 🎉")
            return redirect("order_success", order_id=order.id)

    return render(request, "checkout.html", {
        "cart_items": cart_items,
        "total": total,
    })
