# 🛍️ E-Commerce Platform

A full-featured Django-based e-commerce application with product browsing, cart management, order tracking, product reviews, and online payment integration.

## ✨ Features

### Core Features
- 🏪 **Product Catalog** - Browse products by category with filtering and sorting
- 🛒 **Shopping Cart** - Add, update, remove items with real-time totals
- 👤 **User Authentication** - Register, login, logout with secure password reset
- 📦 **Order Management** - Place orders and track order history
- 🌓 **Dark/Light Mode** - Theme preference saved to browser

### New Features (Added)
- ⭐ **Product Reviews** - 5-star rating system with customer reviews
- 📊 **Order Status Tracking** - Monitor orders through: Pending → Processing → Shipped → Delivered
- 👤 **User Profile** - View account info and complete order history
- 💳 **Razorpay Integration** - Online payments via credit/debit cards, UPI, and Net Banking
- 🔐 **Payment Security** - Secure payment processing with signature verification

## 🛠️ Tech Stack

- **Backend**: Django 5.1+
- **Database**: SQLite (development)
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
- **Images**: Pillow (image processing)
- **Payments**: Razorpay SDK
- **Environment**: python-dotenv

## 📋 Requirements

- Python 3.8+
- Django 4.2+
- Pillow 10.0.0+
- Razorpay 1.3.0+
- python-dotenv 1.0.0+

## 🚀 Quick Start

1. Create a virtual environment and activate it.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run migrations:
   ```bash
   python manage.py migrate
   ```
4. Create a superuser for admin:
   ```bash
   python manage.py createsuperuser
   ```
5. Load sample data (optional):
   ```bash
   python manage.py create_initial_data
   ```
6. Start the development server:
   ```bash
   python manage.py runserver
   ```
7. Visit `http://127.0.0.1:8000/` in your browser

## 🔑 Environment Setup

### For Razorpay Payments

1. **Create `.env` file** from template:
   ```bash
   cp .env.example .env
   ```

2. **Add your Razorpay keys:**
   ```
   RAZORPAY_KEY_ID=your_test_key_id
   RAZORPAY_KEY_SECRET=your_test_key_secret
   ```

3. Get keys from: https://dashboard.razorpay.com/app/settings/api-keys

📖 See `SECURITY_SETUP.md` for detailed security instructions

## 📖 Helpful Guides

- **Features Documentation**: See [FEATURES_SETUP.md](FEATURES_SETUP.md)
  - Order Status Tracking
  - User Profile & Order History
  - Product Reviews System
  - Razorpay Payment Integration

- **Security & Environment Setup**: See [SECURITY_SETUP.md](SECURITY_SETUP.md)
  - Environment variables configuration
  - Razorpay API key setup
  - Security best practices

## 🌐 API Routes

| URL | Purpose |
|-----|---------|
| `/` | Home page |
| `/products/` | Product listing |
| `/product/<id>/` | Product details |
| `/search/?q=term` | Search products |
| `/cart/` | Shopping cart |
| `/cart/add/<id>/` | Add to cart |
| `/checkout/` | Checkout page |
| `/profile/` | User profile & order history |
| `/order/<id>/` | Order details |
| `/product/<id>/review/` | Add/edit product review |
| `/product/<id>/reviews/` | View all reviews |
| `/login/` | User login |
| `/register/` | User registration |
| `/logout/` | User logout |
| `/admin/` | Django admin panel |

## 🗂️ Project Structure

```
ecommerce/
├── manage.py
├── requirements.txt
├── README.md
├── FEATURES_SETUP.md
├── SECURITY_SETUP.md
├── .env.example
├── db.sqlite3
│
├── ecommerce/           # Project settings
│   ├── settings.py      # Django config
│   ├── urls.py          # Main URL routes
│   ├── wsgi.py
│   └── asgi.py
│
├── shop/                # Main Django app
│   ├── models.py        # Database models
│   ├── views.py         # View functions
│   ├── urls.py          # App URL routes
│   ├── forms.py         # Django forms
│   ├── admin.py         # Admin interface
│   └── migrations/      # Database migrations
│
├── templates/           # HTML templates
│   ├── base.html
│   ├── home.html
│   ├── product_detail.html
│   ├── product_list.html
│   ├── cart.html
│   ├── checkout.html
│   ├── profile.html
│   ├── order_detail.html
│   ├── add_review.html
│   ├── product_reviews.html
│   └── razorpay_payment.html
│
├── static/              # CSS, JS, images
│   ├── css/
│   ├── js/
│   └── images/
│
└── media/               # User uploads
    └── product_images/
```

## 🧪 Testing

### Test Account
- Username: `testuser`
- Password: `testpass123`

### Test Payment (Razorpay)
- Card: `4111 1111 1111 1111`
- Expiry: Any future date
- CVV: Any 3 digits

## 🔒 Security Notes

- ✅ Never commit `.env` file to Git
- ✅ Use environment variables for secrets
- ✅ Use test keys for development
- ✅ Enable HTTPS in production
- ✅ Set `DEBUG = False` in production

## 👤 Admin Panel

1. Go to `/admin/`
2. Login with superuser credentials
3. Manage:
   - Products & Categories
   - Orders & Order Items
   - Reviews & Ratings
   - Users

## 🐛 Troubleshooting

**Issue: "ModuleNotFoundError: No module named 'razorpay'"**
```bash
pip install razorpay
```

**Issue: "no such table" error**
```bash
python manage.py migrate
```

**Issue: "Razorpay keys not found"**
- Ensure `.env` file exists in project root
- Verify keys are correct
- Restart Django server

## 📝 Models

### Product
- Name, description, price, category
- Image, rating, stock
- Timestamps (created_at, updated_at)

### Order
- User, total amount, payment method
- Shipping address, order status
- Status choices: pending, processing, shipped, delivered, cancelled

### Review
- Product & User (unique together)
- Rating (1-5 stars), title, comment
- Timestamps

### Cart & CartItem
- One cart per user
- Multiple cart items with quantities

## 🤝 Contributing

Feel free to fork and submit pull requests!

## 📄 License

This project is open source and available under the MIT License.

## 💬 Support

For issues or questions, please open a GitHub issue.

---

**Happy selling! 🎉**
