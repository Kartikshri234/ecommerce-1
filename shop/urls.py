from django.urls import path
from shop.views import (
    # Auth
    register_view, login_view, logout_view,
    # Products
    home, product_list, product_detail, search_products,
    # Cart
    add_to_cart, cart_view, update_cart, remove_from_cart, checkout,
    # Orders
    order_success, order_detail, razorpay_checkout, razorpay_callback,
    # Reviews
    add_review, product_reviews, my_reviews,
    # Profile
    user_profile, edit_profile, manage_addresses,
    add_address, edit_address, delete_address,
    my_wishlist, add_to_wishlist, remove_from_wishlist,
)

urlpatterns = [
    path('', home, name='home'),
    path('products/', product_list, name='product_list'),
    path('search/', search_products, name='search_products'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    path('cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', cart_view, name='cart'),
    path('cart/update/<int:item_id>/', update_cart, name='update_cart'),
    path('cart/remove/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('checkout/', checkout, name='checkout'),
    path('order/success/<int:order_id>/', order_success, name='order_success'),
    
    # Profile & Order History
    path('profile/', user_profile, name='user_profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('order/<int:order_id>/', order_detail, name='order_detail'),
    
    # Addresses
    path('addresses/', manage_addresses, name='manage_addresses'),
    path('addresses/add/', add_address, name='add_address'),
    path('addresses/<int:address_id>/edit/', edit_address, name='edit_address'),
    path('addresses/<int:address_id>/delete/', delete_address, name='delete_address'),
    
    # Wishlist
    path('wishlist/', my_wishlist, name='my_wishlist'),
    path('wishlist/add/<int:product_id>/', add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/', remove_from_wishlist, name='remove_from_wishlist'),
    
    # My Reviews
    path('reviews/', my_reviews, name='my_reviews'),
    
    # Reviews
    path('product/<int:product_id>/review/', add_review, name='add_review'),
    path('product/<int:product_id>/reviews/', product_reviews, name='product_reviews'),
    
    # Razorpay Payment
    path('razorpay/checkout/<int:order_id>/', razorpay_checkout, name='razorpay_checkout'),
    path('razorpay/callback/', razorpay_callback, name='razorpay_callback'),
]
