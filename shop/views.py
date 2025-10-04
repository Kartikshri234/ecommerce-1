from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.db.models import Q

from .models import Product, Cart, CartItem, Order, Category
from .forms import RegisterForm


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
            return redirect("home")
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
            return redirect("home")
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
    return render(request, 'cart.html', {'cart': cart})


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