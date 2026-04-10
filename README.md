# E-Commerce Website

A Django-based e-commerce project with product browsing, media-backed product images, cart management, user authentication, checkout, and an admin panel.

## Features

- Product catalog with categories, filtering, sorting, and detail pages
- Product images stored in `media/product_images`
- Cart add/update/remove flow
- Register, login, logout, and password reset routes
- Checkout and order confirmation
- Django admin for catalog and order management

## Tech Stack

- Django
- SQLite for development
- HTML, CSS, JavaScript
- Pillow for image uploads

## Setup

1. Create a virtual environment and activate it.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run migrations:
   ```bash
   python manage.py migrate
   ```
4. Load sample data:
   ```bash
   python manage.py create_initial_data
   ```
5. Start the app:
   ```bash
   python manage.py runserver
   ```

## Useful URLs

- Home: `/`
- Products: `/products/`
- Cart: `/cart/`
- Login: `/login/`
- Register: `/register/`
- Admin: `/admin/`

## Notes

- The project uses `templates/base.html` for shared navigation.
- Static files live in `static/`.
- User-uploaded product images live in `media/product_images/`.
