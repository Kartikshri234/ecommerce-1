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
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    
    # Reviews
    path('product/<int:product_id>/review/', views.add_review, name='add_review'),
    path('product/<int:product_id>/reviews/', views.product_reviews, name='product_reviews'),
    
    # Razorpay Payment
    path('razorpay/checkout/<int:order_id>/', views.razorpay_checkout, name='razorpay_checkout'),
    path('razorpay/callback/', views.razorpay_callback, name='razorpay_callback'),
]
