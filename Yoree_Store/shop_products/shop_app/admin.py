# shop_app/admin.py
from django.contrib import admin
from .models import  FeaturedProduct, S_product, Product_category

# Register each model individually
admin.site.register(Product_category)
admin.site.register(FeaturedProduct)
admin.site.register(S_product)




