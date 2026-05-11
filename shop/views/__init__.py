# Auth Views
from .auth_views import register_view, login_view, logout_view

# Product Views
from .product_views import home, product_list, product_detail, search_products

# Cart Views
from .cart_views import add_to_cart, cart_view, update_cart, remove_from_cart, checkout

# Order Views
from .order_views import order_success, order_detail, razorpay_checkout, razorpay_callback

# Review Views
from .review_views import add_review, product_reviews, my_reviews

# Profile Views
from .profile_views import (
    user_profile, edit_profile, manage_addresses, 
    add_address, edit_address, delete_address,
    my_wishlist, add_to_wishlist, remove_from_wishlist
)

__all__ = [
    # Auth
    'register_view', 'login_view', 'logout_view',
    # Products
    'home', 'product_list', 'product_detail', 'search_products',
    # Cart
    'add_to_cart', 'cart_view', 'update_cart', 'remove_from_cart', 'checkout',
    # Orders
    'order_success', 'order_detail', 'razorpay_checkout', 'razorpay_callback',
    # Reviews
    'add_review', 'product_reviews', 'my_reviews',
    # Profile
    'user_profile', 'edit_profile', 'manage_addresses',
    'add_address', 'edit_address', 'delete_address',
    'my_wishlist', 'add_to_wishlist', 'remove_from_wishlist',
]
