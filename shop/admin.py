from django.contrib import admin
from .models import Category, Product, Cart, CartItem, Order, OrderItem, Review, UserProfile, SavedAddress, Wishlist

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock', 'rating', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['name', 'description']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at']

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'quantity', 'created_at']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'total_amount', 'payment_method', 'status', 'created_at']
    list_filter = ['created_at', 'payment_method', 'status']
    search_fields = ['user__username', 'shipping_address']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price', 'created_at']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'title', 'created_at']
    list_filter = ['rating', 'created_at', 'product']
    search_fields = ['user__username', 'product__name', 'title', 'comment']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'city', 'created_at']
    search_fields = ['user__username', 'phone', 'city']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(SavedAddress)
class SavedAddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'label', 'city', 'is_default', 'created_at']
    list_filter = ['is_default', 'created_at']
    search_fields = ['user__username', 'city', 'state']


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_product_count', 'created_at']
    search_fields = ['user__username']
    readonly_fields = ['created_at']
    
    def get_product_count(self, obj):
        return obj.products.count()
    get_product_count.short_description = 'Products in Wishlist'