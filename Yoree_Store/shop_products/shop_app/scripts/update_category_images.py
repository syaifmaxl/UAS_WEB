import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Yoree_Store.settings')
django.setup()

from shop_app.models import Product_category

def update_category_images():
    categories = Product_category.objects.all()
    for category in categories:
        # Update the image path as needed
        category.category_img = 'path/to/new/image.jpg'
        category.save()

if __name__ == "__main__":
    update_category_images()
