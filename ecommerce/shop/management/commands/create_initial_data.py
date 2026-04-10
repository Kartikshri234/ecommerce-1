import re
from decimal import Decimal
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from shop.models import Category, Product

class Command(BaseCommand):
    help = 'Creates initial categories and products'

    def handle(self, *args, **kwargs):
        # Create categories
        categories = [
            {'name': 'Electronics', 'slug': 'electronics'},
            {'name': 'Fashion', 'slug': 'fashion'},
            {'name': 'Home & Living', 'slug': 'home-living'},
            {'name': 'Books', 'slug': 'books'},
            {'name': 'Sports', 'slug': 'sports'}
        ]
        
        for cat_data in categories:
            Category.objects.get_or_create(
                name=cat_data['name'],
                slug=cat_data['slug']
            )
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created category "{cat_data["name"]}"')
            )

        media_products_dir = Path(settings.MEDIA_ROOT) / 'product_images'
        if not media_products_dir.exists():
            self.stdout.write(self.style.WARNING(f'No media folder found at {media_products_dir}'))
            return

        category_by_slug = {c.slug: c for c in Category.objects.all()}
        created_products = 0
        updated_products = 0

        for image_path in sorted(media_products_dir.glob('*')):
            if image_path.suffix.lower() not in {'.jpg', '.jpeg', '.png', '.webp'}:
                continue

            product_name = self._humanize_filename(image_path.stem)
            category = self._pick_category(product_name, category_by_slug)
            price = self._derive_price(product_name)
            stock = self._derive_stock(product_name)

            _, created = Product.objects.update_or_create(
                name=product_name,
                defaults={
                    'category': category,
                    'description': f'{product_name} - high quality product available now.',
                    'price': price,
                    'image': f'product_images/{image_path.name}',
                    'stock': stock,
                    'rating': Decimal('4.20'),
                },
            )

            if created:
                created_products += 1
            else:
                updated_products += 1

        self.stdout.write(self.style.SUCCESS(
            f'Products synced from media: created={created_products}, updated={updated_products}'
        ))

    def _humanize_filename(self, stem):
        # Remove random upload suffixes like "_Ab12Xyz" before converting to title case.
        stem = re.sub(r'_[A-Za-z0-9]{6,8}$', '', stem)
        return stem.replace('_', ' ').replace('-', ' ').strip().title()

    def _pick_category(self, name, category_by_slug):
        n = name.lower()
        if any(word in n for word in ['shirt', 'shoes', 'jeans', 'jacket', 'hoodie']):
            return category_by_slug['fashion']
        if any(word in n for word in ['fryer', 'vacuum', 'pot', 'blender', 'kitchen', 'home']):
            return category_by_slug['home-living']
        if any(word in n for word in ['book', 'novel', 'guide']):
            return category_by_slug['books']
        if any(word in n for word in ['sports', 'fitness', 'yoga', 'cycle']):
            return category_by_slug['sports']
        return category_by_slug['electronics']

    def _derive_price(self, name):
        base = Decimal('799.00')
        n = name.lower()
        if any(word in n for word in ['iphone', 'macbook', 'laptop', 'playstation', 'xbox', 'tv', 'camera']):
            return Decimal('69999.00')
        if any(word in n for word in ['headphone', 'speaker', 'watch', 'airpods']):
            return Decimal('7999.00')
        if any(word in n for word in ['shirt', 'shoes', 'jeans']):
            return Decimal('1999.00')
        return base

    def _derive_stock(self, name):
        n = name.lower()
        if any(word in n for word in ['iphone', 'macbook', 'playstation', 'xbox']):
            return 8
        if any(word in n for word in ['laptop', 'camera', 'tv']):
            return 12
        return 25