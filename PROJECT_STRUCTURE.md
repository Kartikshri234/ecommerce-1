# eCommerce Project Structure

## Project Overview
This is a Django-based eCommerce application with clean, modular architecture for easy maintenance and scalability.

---

## Project Root Structure

```
d:\my programs and projects\ecommerce/
├── .env.example              # Environment configuration template
├── .git/                     # Git repository
├── .gitignore                # Git ignore rules
├── db.sqlite3                # SQLite database
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── README.md                 # Main project documentation
├── SECURITY_SETUP.md         # Security configuration guide
├── FIXES_SUMMARY.md          # Summary of applied fixes
├── logs/                     # Application logs
├── media/                    # User uploaded files
├── ecommerce/                # Django project settings
├── shop/                     # Django app (main application)
├── static/                   # Static assets (CSS, JS, images)
├── staticfiles/              # Collected static files
└── templates/                # HTML templates
```

---

## Django App Structure - `shop/`

```
shop/
├── views/                    # Refactored views (modular)
│   ├── __init__.py          # Exports all views
│   ├── auth_views.py        # Authentication (register, login, logout)
│   ├── product_views.py     # Product listing & search
│   ├── cart_views.py        # Cart management & checkout
│   ├── order_views.py       # Order processing & Razorpay payment
│   ├── review_views.py      # Product reviews
│   └── profile_views.py     # User profile & address management
├── migrations/              # Database migrations
├── management/              # Custom management commands
├── __init__.py
├── admin.py                 # Django admin configuration
├── apps.py                  # App configuration
├── context_processors.py    # Template context processors
├── forms.py                 # Django forms
├── models.py                # Database models
├── tests.py                 # Test cases
├── urls.py                  # URL routing
└── pycache__/
```

---

## Views Module Structure

The `shop/views/` directory is organized by functionality:

### 1. `auth_views.py` - Authentication
- `register_view()` - User registration
- `login_view()` - User login
- `logout_view()` - User logout

### 2. `product_views.py` - Product Management
- `home()` - Home page with featured products
- `product_list()` - List all products with filtering & sorting
- `product_detail()` - Display product details
- `search_products()` - Full-text search

### 3. `cart_views.py` - Shopping Cart
- `add_to_cart()` - Add product to cart (AJAX)
- `cart_view()` - Display shopping cart
- `update_cart()` - Update item quantity
- `remove_from_cart()` - Remove item from cart
- `checkout()` - Process checkout & create order

### 4. `order_views.py` - Order Processing
- `order_success()` - Order confirmation page
- `order_detail()` - View order details
- `razorpay_checkout()` - Initiate Razorpay payment
- `razorpay_callback()` - Handle Razorpay payment callback

### 5. `review_views.py` - Product Reviews
- `add_review()` - Create/edit product review
- `product_reviews()` - Display all reviews for product
- `my_reviews()` - View user's all reviews

### 6. `profile_views.py` - User Profile
- `user_profile()` - Display user profile with statistics
- `edit_profile()` - Edit profile information
- `manage_addresses()` - Manage saved addresses
- `add_address()` - Add new address
- `edit_address()` - Edit existing address
- `delete_address()` - Delete address
- `my_wishlist()` - View user's wishlist
- `add_to_wishlist()` - Add product to wishlist
- `remove_from_wishlist()` - Remove from wishlist

---

## Django Project Settings - `ecommerce/`

```
ecommerce/
├── __init__.py
├── asgi.py           # ASGI configuration (for production)
├── wsgi.py           # WSGI configuration
├── settings.py       # Main Django settings
└── urls.py           # Root URL configuration
```

### Key Features in settings.py:
- ✅ Environment-based configuration (DEBUG, SECRET_KEY, ALLOWED_HOSTS)
- ✅ Production security headers (SSL, secure cookies, CSP)
- ✅ Logging configuration with file & console handlers
- ✅ Static and media file configuration

---

## Templates - `templates/`

```
templates/
├── base.html                 # Base template with navigation
├── home.html                 # Home page
├── product_list.html         # Product listing
├── product_detail.html       # Product details
├── search_results.html       # Search results
├── cart.html                 # Shopping cart
├── checkout.html             # Checkout form
├── order_detail.html         # Order details
├── order_success.html        # Order confirmation
├── login.html                # Login page
├── register.html             # Registration page
├── profile.html              # User profile dashboard
├── edit_profile.html         # Edit profile
├── add_review.html           # Add/edit review
├── product_reviews.html      # View product reviews
├── my_reviews.html           # User's reviews
├── wishlist.html             # Wishlist page
├── manage_addresses.html     # Address management
├── add_address.html          # Add address form
├── edit_address.html         # Edit address form
├── razorpay_payment.html     # Razorpay payment page
└── registration/             # Auth templates
    ├── password_reset_form.html
    ├── password_reset_done.html
    ├── password_reset_confirm.html
    └── password_reset_complete.html
```

---

## Static Files - `static/`

```
static/
├── css/
│   └── style.css             # Main stylesheet
├── js/
│   ├── main.js               # Main JavaScript (cart, theme, etc)
│   └── product_list.js       # Product filter functionality
└── images/
    ├── icons/                # Icon images
    └── products/             # Product images
```

---

## Media Files - `media/`

```
media/
└── product_images/           # User-uploaded product images
```

---

## Database - `db.sqlite3`

SQLite database containing:
- Users & authentication
- Products & categories
- Shopping carts & cart items
- Orders & order items
- Reviews
- User profiles & saved addresses
- Wishlists

---

## Configuration Files

### `.env.example`
Environment variable template with:
- Django settings (DEBUG, SECRET_KEY, ALLOWED_HOSTS)
- Razorpay credentials
- Optional email & database configs

### `requirements.txt`
Python dependencies:
- Django
- python-decouple (for environment variables)
- razorpay (payment gateway)
- Pillow (image handling)

### `SECURITY_SETUP.md`
Security configuration guide for:
- SSL/HTTPS setup
- Secret key generation
- Allowed hosts configuration

### `FIXES_SUMMARY.md`
Complete summary of all applied fixes and improvements

---

## URL Routing - `shop/urls.py`

Organized by functionality:
- `/` - Home
- `/products/` - Product listing
- `/product/<id>/` - Product detail
- `/search/` - Search products
- `/cart/` - Cart operations
- `/checkout/` - Checkout
- `/order/` - Order management
- `/profile/` - User profile
- `/addresses/` - Address management
- `/wishlist/` - Wishlist management
- `/reviews/` - Review management
- `/razorpay/` - Payment processing

---

## Models - `shop/models.py`

### Core Models:
1. **Category** - Product categories
2. **Product** - Product catalog
3. **User** - Django User model
4. **UserProfile** - Extended user information
5. **Cart** - Shopping cart (1-to-1 with User)
6. **CartItem** - Items in cart
7. **Order** - Purchase orders
8. **OrderItem** - Items in order
9. **Review** - Product reviews
10. **SavedAddress** - Saved shipping addresses
11. **Wishlist** - User wishlists

---

## Forms - `shop/forms.py`

- `RegisterForm` - User registration
- `ReviewForm` - Product review submission
- `UserProfileForm` - Profile information
- `SavedAddressForm` - Address information

---

## Key Features

### 🔐 Security
- Environment-based configuration
- HTTPS/SSL ready
- CSRF protection
- XSS filter enabled
- Content Security Policy headers
- Secure session cookies
- Input validation & sanitization

### 💳 Payment Integration
- Razorpay payment gateway integration
- Payment callback verification
- Order status tracking

### 📦 E-Commerce Features
- Product catalog with categories
- Full-text search
- Shopping cart management
- Inventory tracking
- Order management
- Product reviews with ratings
- Wishlist functionality

### 👤 User Management
- User registration & authentication
- Profile management
- Multiple saved addresses
- Order history
- Review history
- Wishlist management

### 🎨 Frontend
- Responsive design
- Dark mode support
- Smooth animations
- AJAX functionality
- Lazy image loading

---

## Installation & Setup

### 1. Clone Repository
```bash
git clone <repo-url>
cd ecommerce
```

### 2. Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
```bash
cp .env.example .env
# Edit .env with your settings
```

### 5. Database Setup
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 6. Collect Static Files
```bash
python manage.py collectstatic
```

### 7. Run Development Server
```bash
python manage.py runserver
```

---

## Testing

### Run Tests
```bash
python manage.py test
```

### Security Check
```bash
python manage.py check --deploy
```

---

## Deployment

1. Set `DEBUG=False` in .env
2. Generate secure SECRET_KEY
3. Configure ALLOWED_HOSTS
4. Run `python manage.py check --deploy`
5. Set up HTTPS/SSL
6. Configure production web server (Gunicorn/Nginx)
7. Set up email configuration (optional)
8. Monitor logs in `logs/django.log`

---

## Best Practices Applied

✅ **Separation of Concerns** - Views organized by functionality  
✅ **DRY Principle** - No duplicate code  
✅ **Security First** - Environment-based config, input validation  
✅ **Error Handling** - Specific exception handling with logging  
✅ **Code Organization** - Modular, easy to maintain structure  
✅ **Documentation** - Clear comments and docstrings  
✅ **Scalability** - Ready for growth and additional features  

---

## Troubleshooting

### Views Module Not Found
- Ensure `shop/views/__init__.py` exists with all imports

### Import Errors
- Verify all view files are in `shop/views/` directory
- Check imports in `shop/views/__init__.py`

### Database Issues
- Run migrations: `python manage.py migrate`
- Reset database: `python manage.py migrate --zero <app_label>`

### Static Files Not Loading
- Run: `python manage.py collectstatic`
- Check STATIC_ROOT and STATIC_URL in settings

---

**Last Updated:** 2024-01-XX  
**Version:** 2.0 (Refactored with modular views)
