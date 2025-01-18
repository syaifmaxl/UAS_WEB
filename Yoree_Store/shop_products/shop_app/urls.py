from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .import views


urlpatterns = [
    path('', views.index, name = 'index'),
    path('contact', views.contact, name = 'contact'),
    path('shop', views.shop, name = 'shop'),
    path('details' , views.detail, name='details'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('cart_page/', views.cart_page, name='cart_page'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('thank_you/', views.thank_you, name='thank_you'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('logout/', views.logout, name='logout'),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)