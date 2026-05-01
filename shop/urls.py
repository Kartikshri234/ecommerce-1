from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('search/', views.search_products, name='search_products'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/update/<int:item_id>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('checkout/', views.checkout, name='checkout'),
    path('order/success/<int:order_id>/', views.order_success, name='order_success'),
    
    # Profile & Order History
    path('profile/', views.user_profile, name='user_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    
    # Addresses
    path('addresses/', views.manage_addresses, name='manage_addresses'),
    path('addresses/add/', views.add_address, name='add_address'),
    path('addresses/<int:address_id>/edit/', views.edit_address, name='edit_address'),
    path('addresses/<int:address_id>/delete/', views.delete_address, name='delete_address'),
    
    # Wishlist
    path('wishlist/', views.my_wishlist, name='my_wishlist'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    
    # My Reviews
    path('reviews/', views.my_reviews, name='my_reviews'),
    
    # Reviews
    path('product/<int:product_id>/review/', views.add_review, name='add_review'),
    path('product/<int:product_id>/reviews/', views.product_reviews, name='product_reviews'),
    
    # Razorpay Payment
    path('razorpay/checkout/<int:order_id>/', views.razorpay_checkout, name='razorpay_checkout'),
    path('razorpay/callback/', views.razorpay_callback, name='razorpay_callback'),
]
