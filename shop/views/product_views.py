"""Product Views - Home, Listing, Search"""
from django.shortcuts import render, get_object_or_404
from django.db.models import Q

from shop.models import Product, Category


def home(request):
    """Display home page with featured products"""
    products = Product.objects.all()[:8]  # show featured / latest
    return render(request, "home.html", {"products": products})


def product_list(request):
    """List all products with filtering and sorting"""
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
    """Display product details"""
    product = get_object_or_404(Product, id=product_id)
    return render(request, "product_detail.html", {"product": product})


def search_products(request):
    """Search for products by name, description, or category"""
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
