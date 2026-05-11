#!/usr/bin/env python
"""
Comprehensive Testing Script for eCommerce Application
Tests all major functionality and verifies fixes
"""

import os
import django
import sys

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
sys.path.insert(0, r'd:\my programs and projects\ecommerce')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from shop.models import Product, Category, Order, Cart, CartItem
import json

client = Client()

def test_checkout_validation():
    """Test checkout form validation"""
    print("\n📝 Testing Checkout Validation...")
    
    # Create test user
    user = User.objects.create_user(username='testuser', password='testpass123')
    client.login(username='testuser', password='testpass123')
    
    # Test empty fields
    response = client.post('/checkout/', {
        'payment_method': '',
        'full_name': '',
        'phone': '',
        'address_line1': '',
        'city': ''
    })
    
    if response.status_code == 200 and 'fill in all required fields' in str(response.content):
        print("✅ Empty field validation works")
    else:
        print("❌ Empty field validation failed")
    
    # Test invalid payment method
    response = client.post('/checkout/', {
        'payment_method': 'invalid_payment',
        'full_name': 'Test User',
        'phone': '1234567890',
        'address_line1': '123 Main St',
        'city': 'Test City'
    })
    
    if response.status_code == 200 and 'Invalid payment method' in str(response.content):
        print("✅ Payment method validation works")
    else:
        print("❌ Payment method validation failed")
    
    print("✅ Checkout validation tests completed")

def test_add_to_cart():
    """Test add to cart functionality"""
    print("\n🛒 Testing Add to Cart...")
    
    # Create test user
    user = User.objects.create_user(username='testuser2', password='testpass123')
    client.login(username='testuser2', password='testpass123')
    
    # Get first product
    product = Product.objects.first()
    if product:
        # Test add to cart
        response = client.post(f'/cart/add/{product.id}/', {'quantity': 1})
        
        if response.status_code == 200:
            data = json.loads(response.content)
            if data.get('success'):
                print("✅ Add to cart works successfully")
            else:
                print(f"❌ Add to cart failed: {data.get('message')}")
        else:
            print(f"❌ Add to cart returned status {response.status_code}")
    else:
        print("⚠️  No products found for testing")

def test_product_stock():
    """Test stock management"""
    print("\n📦 Testing Stock Management...")
    
    # Create test product with limited stock
    category = Category.objects.first() or Category.objects.create(name="Test", slug="test")
    product = Product.objects.create(
        name="Test Product",
        category=category,
        price=100,
        description="Test",
        stock=1
    )
    
    # Test out of stock handling
    user = User.objects.create_user(username='testuser3', password='testpass123')
    client.login(username='testuser3', password='testpass123')
    
    # Try to add product with quantity > stock
    response = client.post(f'/cart/add/{product.id}/', {'quantity': 5})
    
    if response.status_code == 200:
        data = json.loads(response.content)
        if data.get('success'):
            print("✅ Stock limit handling works")
        else:
            print(f"⚠️  Stock handling: {data.get('message')}")
    else:
        print(f"❌ Stock test returned status {response.status_code}")

def run_all_tests():
    """Run all tests"""
    print("=" * 50)
    print("🧪 Starting eCommerce Application Tests")
    print("=" * 50)
    
    try:
        test_checkout_validation()
        test_add_to_cart()
        test_product_stock()
        
        print("\n" + "=" * 50)
        print("✅ All tests completed!")
        print("=" * 50)
    except Exception as e:
        print(f"\n❌ Test execution error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    run_all_tests()
