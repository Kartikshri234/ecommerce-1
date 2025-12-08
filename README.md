# E-Commerce Website - Django Project

A full-featured e-commerce web application built with Django, inspired by popular platforms like Amazon and Flipkart. This project provides a complete online shopping experience with product browsing, cart management, user authentication, and order processing.

## 🌟 Features

### Core Functionality
- **Product Management**: Browse products with detailed information including images, prices, ratings, and stock availability
- **Category System**: Products organized by categories for easy navigation
- **Search & Filtering**: Sort products by price (ascending/descending) and rating
- **Product Details**: Comprehensive product pages with descriptions and specifications

### Shopping Cart
- **Dynamic Cart**: Real-time cart updates using AJAX
- **Cart Management**: Add, update quantity, and remove items
- **Stock Validation**: Automatic stock checking to prevent overselling
- **Cart Counter**: Live cart item count in navigation

### User Authentication
- **User Registration**: Secure user registration with email validation
- **Login/Logout**: Session-based authentication
- **Password Reset**: Email-based password recovery system
- **Protected Routes**: Login required for cart and checkout operations

### Checkout & Orders
- **Secure Checkout**: Multi-step checkout process
- **Multiple Payment Methods**: Cash on Delivery (COD) and online payment options
- **Shipping Information**: Comprehensive address collection
- **Order History**: Users can track their orders
- **Stock Management**: Automatic inventory updates after order placement
- **Order Confirmation**: Success page with order details

### Admin Panel
- **Django Admin**: Full-featured admin interface
- **Product Management**: Add, edit, and delete products
- **Category Management**: Organize product categories
- **Order Management**: View and manage customer orders
- **User Management**: Manage registered users

## 🛠️ Technology Stack

- **Backend**: Django 3.x (Python Web Framework)
- **Database**: SQLite3 (Development) - Easily upgradeable to PostgreSQL/MySQL
- **Frontend**: HTML5, CSS3, JavaScript
- **Styling**: Custom CSS with responsive design
- **Image Handling**: Pillow library for image processing
- **Authentication**: Django's built-in authentication system

## 📁 Project Structure

```
claude/
├── ecommerce/              # Main project directory
│   ├── settings.py         # Django settings
│   ├── urls.py            # Root URL configuration
│   ├── wsgi.py            # WSGI configuration
│   └── asgi.py            # ASGI configuration
├── shop/                  # Main application
│   ├── models.py          # Database models (Product, Cart, Order, etc.)
│   ├── views.py           # View functions
│   ├── urls.py            # App URL patterns
│   ├── forms.py           # Django forms
│   ├── admin.py           # Admin configuration
│   ├── context_processors.py  # Custom context processors
│   └── management/
│       └── commands/
│           └── create_initial_data.py  # Data seeding command
├── templates/             # HTML templates
│   ├── base.html          # Base template
│   ├── home.html          # Homepage
│   ├── product_list.html  # Product listing
│   ├── product_detail.html # Product details
│   ├── cart.html          # Shopping cart
│   ├── checkout.html      # Checkout page
│   ├── order_success.html # Order confirmation
│   ├── login.html         # Login page
│   ├── register.html      # Registration page
│   └── registration/      # Password reset templates
├── static/                # Static files
│   ├── css/
│   │   └── style.css      # Custom styles
│   ├── js/
│   │   ├── main.js        # Main JavaScript
│   │   └── product_list.js # Product list functionality
│   └── images/            # Static images
├── media/                 # User-uploaded files
│   └── product_images/    # Product images
├── db.sqlite3             # SQLite database
├── manage.py              # Django management script
└── README.md              # Project documentation
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Step-by-Step Installation

1. **Clone the repository** (or download the project)
   ```bash
   cd C:\Users\karti\OneDrive\Desktop\claude
   ```

2. **Create and activate virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install required packages**
   ```bash
   pip install django
   pip install Pillow  # For image handling
   ```

4. **Apply database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser (admin account)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Load initial data (optional)**
   ```bash
   python manage.py create_initial_data
   ```

7. **Collect static files**
   ```bash
   python manage.py collectstatic
   ```

8. **Run development server**
   ```bash
   python manage.py runserver
   ```

9. **Access the application**
   - Website: http://127.0.0.1:8000/
   - Admin Panel: http://127.0.0.1:8000/admin/

## 📊 Database Models

### Product
- Name, description, price
- Category (Foreign Key)
- Image, rating, stock
- Timestamps (created_at, updated_at)

### Category
- Name, slug
- Used for product organization

### Cart & CartItem
- User-specific shopping cart
- Multiple items with quantities
- Automatic total calculation

### Order & OrderItem
- Complete order information
- Payment method, shipping address
- Order items with prices locked at purchase time
- Order history and tracking

## 🎨 Key Features Implementation

### AJAX Cart Operations
- Add to cart without page reload
- Real-time cart count updates
- Instant feedback messages

### Stock Management
- Stock validation before adding to cart
- Automatic stock reduction on order placement
- Out-of-stock indicators

### Responsive Design
- Mobile-friendly interface
- Adaptive layouts for different screen sizes
- Touch-optimized controls

### Security Features
- CSRF protection on all forms
- Login required decorators for sensitive operations
- Password validation
- Secure session management

## 🔧 Configuration

### Important Settings (settings.py)
- `SECRET_KEY`: Change in production
- `DEBUG`: Set to False in production
- `ALLOWED_HOSTS`: Configure for deployment
- `DATABASES`: Upgrade to PostgreSQL for production
- `STATIC_ROOT` & `MEDIA_ROOT`: Configure paths

### Environment Variables (Recommended)
Create a `.env` file for sensitive information:
```
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=your-database-url
```

## 📝 Usage

### For Customers
1. Browse products on homepage or product listing page
2. Filter by category or sort by price/rating
3. Click on product for detailed information
4. Add items to cart (login required)
5. Review cart and update quantities
6. Proceed to checkout
7. Fill shipping information
8. Select payment method
9. Place order and receive confirmation

### For Administrators
1. Access admin panel at `/admin/`
2. Add/edit products and categories
3. Manage user accounts
4. View and process orders
5. Monitor inventory levels

## 🚀 Future Enhancements

- [ ] Product reviews and ratings system
- [ ] Wishlist functionality
- [ ] Advanced search with filters
- [ ] Multiple payment gateway integration
- [ ] Order tracking system
- [ ] Email notifications
- [ ] Product recommendations
- [ ] Coupon and discount system
- [ ] Multi-vendor support
- [ ] Invoice generation
- [ ] Advanced analytics dashboard

## 🐛 Known Issues & Limitations

- Currently uses SQLite (not recommended for production)
- Payment integration is COD only (needs payment gateway)
- No email functionality configured
- Limited error handling in some views

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available for educational purposes.

## 👨‍💻 Developer

Developed as a comprehensive Django e-commerce project demonstrating full-stack web development skills.

## 📞 Support

For questions or issues, please create an issue in the repository.

---

**Note**: This is a development version. Before deploying to production, ensure you:
- Change SECRET_KEY
- Set DEBUG = False
- Configure proper database (PostgreSQL recommended)
- Set up proper static/media file serving
- Configure HTTPS
- Set up proper email backend
- Implement proper error logging
- Add security headers
- Configure ALLOWED_HOSTS

Happy Shopping! 🛍️
