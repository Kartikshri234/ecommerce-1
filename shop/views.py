from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.db.models import Q, Avg, Sum
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from .models import Product, Cart, CartItem, Order, Category, Review, UserProfile, SavedAddress, Wishlist
from .forms import RegisterForm, ReviewForm, UserProfileForm, SavedAddressForm


# ------------------------
# Home & Products
# ------------------------

def home(request):
    products = Product.objects.all()[:8]  # show featured / latest
    return render(request, "home.html", {"products": products})


def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    
    # Filter by category
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)
    
    # Sort products
    sort = request.GET.get('sort')
    if sort:
        if sort == 'price_asc':
            products = products.order_by('price')
        elif sort == 'price_desc':
            products = products.order_by('-price')
        elif sort == 'rating_desc':
            products = products.order_by('-rating')
    
    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'product_list.html', context)


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, "product_detail.html", {"product": product})


def search_products(request):
    query = (request.GET.get('q') or '').strip()
    products = Product.objects.none()

    if query:
        products = Product.objects.filter(
            Q(name__icontains=query)
            | Q(description__icontains=query)
            | Q(category__name__icontains=query)
        ).distinct()

    return render(request, 'search_results.html', {
        'query': query,
        'products': products,
    })


# ------------------------
# Authentication
# ------------------------

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful! 🎉")
            return redirect(request.GET.get("next") or "home")
        messages.error(request, "Please fix the errors below and try again.")
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back {user.username}!")
            return redirect(request.GET.get("next") or "home")
        else:
            messages.error(request, "Invalid username or password ❌")
    return render(request, "login.html")


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("home")


# ------------------------
# Cart
# ------------------------

@login_required
def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)

        if product.stock <= 0:
            return JsonResponse({
                'success': False,
                'message': 'Product is out of stock ❌'
            })

        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={"quantity": 1},
        )

        if not created:
            if cart_item.quantity < product.stock:
                cart_item.quantity += 1
                cart_item.save()
                message = f"Increased {product.name} quantity in cart!"
            else:
                message = f"Stock limit reached for {product.name}"
        else:
            message = f"{product.name} added to cart!"

        return JsonResponse({
            'success': True,
            'cart_count': cart.get_total_items(),
            'message': message
        })
    
    return JsonResponse({
        'success': False,
        'message': 'Invalid request'
    })

@login_required
def cart_view(request):
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
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    messages.info(request, "Item removed from cart.")
    return redirect("cart")


# ------------------------
# Checkout & Orders
# ------------------------

@login_required
def checkout(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    if not cart_items.exists():
        messages.warning(request, "Your cart is empty!")
        return redirect("product_list")

    total = sum(item.get_total() for item in cart_items)

    if request.method == "POST":
        payment_method = request.POST.get("payment_method")
        full_name = request.POST.get("full_name")
        phone = request.POST.get("phone")
        address = request.POST.get("address_line1")
        city = request.POST.get("city")

        # ✅ create order using total_amount field
        order = Order.objects.create(
            user=request.user,
            total_amount=total,
            payment_method=payment_method,
            shipping_address=f"{full_name}, {phone}, {address}, {city}",
        )

        # ✅ move cart items into order
        for item in cart_items:
            order.items.create(
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
            )
            # reduce stock
            item.product.stock -= item.quantity
            item.product.save()

        # ✅ clear cart
        cart_items.delete()

        # ✅ Redirect to Razorpay if payment method is Razorpay
        if payment_method == 'razorpay':
            return redirect('razorpay_checkout', order_id=order.id)
        else:
            messages.success(request, "Order placed successfully! 🎉")
            return redirect("order_success", order_id=order.id)

    return render(request, "checkout.html", {
        "cart_items": cart_items,
        "total": total,
    })


@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "order_success.html", {"order": order})


# ------------------------
# User Profile & Order History
# ------------------------

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order_detail.html', {'order': order})


# ------------------------
# Product Reviews
# ------------------------

@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Check if user already reviewed this product
    existing_review = Review.objects.filter(product=product, user=request.user).first()
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=existing_review)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            
            # Update product average rating
            avg_rating = product.reviews.aggregate(
                avg_rating=Avg('rating')
            )['avg_rating']
            product.rating = avg_rating
            product.save()
            
            messages.success(request, "Review posted successfully! ⭐")
            return redirect('product_detail', product_id=product.id)
    else:
        form = ReviewForm(instance=existing_review)
    
    return render(request, 'add_review.html', {
        'form': form,
        'product': product,
        'existing_review': existing_review,
    })


def product_reviews(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = product.reviews.all()
    return render(request, 'product_reviews.html', {
        'product': product,
        'reviews': reviews,
    })


# ------------------------
# Razorpay Integration
# ------------------------

@login_required
def razorpay_checkout(request, order_id):
    """Initiate Razorpay payment for an order"""
    import razorpay
    
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if order.payment_method != 'razorpay':
        messages.error(request, "Invalid payment method for this order")
        return redirect('order_detail', order_id=order.id)
    
    # Initialize Razorpay client
    client = razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
    )
    
    # Create payment order
    razorpay_order = client.order.create(
        amount=int(float(order.total_amount) * 100),  # Amount in paise
        currency='INR',
        receipt=f'order_{order.id}',
    )
    
    context = {
        'order': order,
        'razorpay_order': razorpay_order,
        'razorpay_key': settings.RAZORPAY_KEY_ID,
    }
    
    return render(request, 'razorpay_payment.html', context)


@login_required
@csrf_exempt
def razorpay_callback(request):
    """Handle Razorpay payment callback"""
    import razorpay
    
    if request.method == 'POST':
        try:
            payment_details = {
                'razorpay_order_id': request.POST.get('razorpay_order_id'),
                'razorpay_payment_id': request.POST.get('razorpay_payment_id'),
                'razorpay_signature': request.POST.get('razorpay_signature'),
            }
            
            # Verify payment signature
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            client.utility.verify_payment_signature(payment_details)
            
            # Update order status
            order_id = request.POST.get('order_id')
            order = Order.objects.get(id=order_id, user=request.user)
            order.status = 'processing'
            order.save()
            
            messages.success(request, "Payment successful! ✅")
            return redirect('order_success', order_id=order.id)
        
        except Exception as e:
            messages.error(request, f"Payment failed: {str(e)}")
            return redirect('cart')


# ------------------------
# Enhanced Profile Features
# ------------------------

@login_required
def user_profile(request):
    """Enhanced profile with statistics and features"""
    user_profile, _ = UserProfile.objects.get_or_create(user=request.user)
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    reviews = Review.objects.filter(user=request.user).order_by('-created_at')
    wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
    saved_addresses = SavedAddress.objects.filter(user=request.user)
    
    # Calculate statistics
    total_spent = orders.aggregate(total=Sum('total_amount'))['total'] or 0
    total_orders = orders.count()
    total_reviews = reviews.count()
    wishlist_count = wishlist.get_total_items()
    
    context = {
        'user': request.user,
        'user_profile': user_profile,
        'orders': orders[:5],  # Latest 5 orders
        'reviews': reviews[:3],  # Latest 3 reviews
        'wishlist': wishlist,
        'saved_addresses': saved_addresses,
        'total_spent': total_spent,
        'total_orders': total_orders,
        'total_reviews': total_reviews,
        'wishlist_count': wishlist_count,
    }
    return render(request, 'profile.html', context)


@login_required
def edit_profile(request):
    """Edit user profile information"""
    user_profile, _ = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            profile = form.save()
            
            # Update User model fields
            request.user.first_name = form.cleaned_data.get('first_name', '')
            request.user.last_name = form.cleaned_data.get('last_name', '')
            request.user.email = form.cleaned_data.get('email', '')
            request.user.save()
            
            messages.success(request, "Profile updated successfully! ✅")
            return redirect('user_profile')
    else:
        form = UserProfileForm(instance=user_profile, initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        })
    
    return render(request, 'edit_profile.html', {'form': form})


@login_required
def manage_addresses(request):
    """Manage saved addresses"""
    saved_addresses = SavedAddress.objects.filter(user=request.user)
    return render(request, 'manage_addresses.html', {'addresses': saved_addresses})


@login_required
def add_address(request):
    """Add a new saved address"""
    if request.method == 'POST':
        form = SavedAddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            
            # If this is set as default, unset others
            if address.is_default:
                SavedAddress.objects.filter(user=request.user).update(is_default=False)
            
            address.save()
            messages.success(request, "Address added successfully! ✅")
            return redirect('manage_addresses')
    else:
        form = SavedAddressForm()
    
    return render(request, 'add_address.html', {'form': form})


@login_required
def edit_address(request, address_id):
    """Edit a saved address"""
    address = get_object_or_404(SavedAddress, id=address_id, user=request.user)
    
    if request.method == 'POST':
        form = SavedAddressForm(request.POST, instance=address)
        if form.is_valid():
            updated_address = form.save(commit=False)
            
            # If this is set as default, unset others
            if updated_address.is_default:
                SavedAddress.objects.filter(user=request.user).exclude(id=address.id).update(is_default=False)
            
            updated_address.save()
            messages.success(request, "Address updated successfully! ✅")
            return redirect('manage_addresses')
    else:
        form = SavedAddressForm(instance=address)
    
    return render(request, 'edit_address.html', {'form': form, 'address': address})


@login_required
def delete_address(request, address_id):
    """Delete a saved address"""
    address = get_object_or_404(SavedAddress, id=address_id, user=request.user)
    address.delete()
    messages.info(request, "Address deleted.")
    return redirect('manage_addresses')


@login_required
def my_wishlist(request):
    """View user's wishlist"""
    wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
    wishlist_products = wishlist.products.all()
    
    return render(request, 'wishlist.html', {
        'wishlist': wishlist,
        'products': wishlist_products,
        'count': wishlist.get_total_items(),
        'total_value': wishlist.get_total_savings(),
    })


@login_required
def add_to_wishlist(request, product_id):
    """Add product to wishlist"""
    product = get_object_or_404(Product, id=product_id)
    wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
    
    if wishlist.products.filter(id=product.id).exists():
        wishlist.products.remove(product)
        return JsonResponse({
            'success': True,
            'message': f"Removed from wishlist",
            'in_wishlist': False,
        })
    else:
        wishlist.products.add(product)
        return JsonResponse({
            'success': True,
            'message': f"Added to wishlist ❤️",
            'in_wishlist': True,
        })


@login_required
def remove_from_wishlist(request, product_id):
    """Remove product from wishlist"""
    product = get_object_or_404(Product, id=product_id)
    wishlist = get_object_or_404(Wishlist, user=request.user)
    wishlist.products.remove(product)
    messages.info(request, "Removed from wishlist.")
    return redirect('my_wishlist')


@login_required
def my_reviews(request):
    """View all user's reviews"""
    reviews = Review.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'my_reviews.html', {'reviews': reviews})