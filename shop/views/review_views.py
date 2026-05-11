"""Review Views"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg

from shop.models import Product, Review
from shop.forms import ReviewForm


@login_required
def add_review(request, product_id):
    """Add or update product review"""
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
    """Display all reviews for a product"""
    product = get_object_or_404(Product, id=product_id)
    reviews = product.reviews.all()
    return render(request, 'product_reviews.html', {
        'product': product,
        'reviews': reviews,
    })


@login_required
def my_reviews(request):
    """View all user's reviews"""
    reviews = Review.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'my_reviews.html', {'reviews': reviews})
