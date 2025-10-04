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