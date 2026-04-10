# File Structure

```text
ecommerce/
├── manage.py
├── db.sqlite3
├── README.md
├── requirements.txt
├── FILE_STRUCTURE.md
├── ecommerce/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── shop/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── context_processors.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   ├── management/
│   │   └── commands/
│   │       └── create_initial_data.py
│   └── migrations/
│       └── 0001_initial.py
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── product_list.html
│   ├── product_detail.html
│   ├── cart.html
│   ├── checkout.html
│   ├── order_success.html
│   ├── login.html
│   ├── register.html
│   └── registration/
├── static/
│   ├── css/
│   ├── js/
│   └── images/
└── media/
    └── product_images/
```