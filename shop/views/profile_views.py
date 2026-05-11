"""Profile & User Management Views"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Sum

from shop.models import (
    UserProfile, Order, Review, SavedAddress, Wishlist
)
from shop.forms import UserProfileForm, SavedAddressForm


@login_required
def user_profile(request):
    """Display user profile with statistics"""
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
    from shop.models import Product
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
    from shop.models import Product
    product = get_object_or_404(Product, id=product_id)
    wishlist = get_object_or_404(Wishlist, user=request.user)
    wishlist.products.remove(product)
    messages.info(request, "Removed from wishlist.")
    return redirect('my_wishlist')
