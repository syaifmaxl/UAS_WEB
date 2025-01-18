from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from decimal import Decimal
from django.contrib import messages 
from .forms import BillingAddressForm, PaymentMethodForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    # Fetch featured products and categories
    featured_products = FeaturedProduct.objects.all()
    categ = Product_category.objects.all()
    
    # Pass both to the template
    return render(request, 'index.html', {
        'featured_products': featured_products,
        'categ': categ
    })

@login_required
def contact(request):
    return render(request,'contact.html')

@login_required
def shop(request):  
    shopproduct = S_product.objects.all()  
    return render(request, 'shop.html',{'shopproduct' : shopproduct})

@login_required
def detail(request):
    shopproduct = S_product.objects.all()  
    return render(request,'details.html',{'shopproduct' : shopproduct})  

@login_required
def product_detail(request, id):
    product = get_object_or_404(S_product, id=id)   
    return render(request, 'details.html', {'product': product})

@login_required
def cart_page(request):
    cart = request.session.get('cart', {})

    total_price = sum(float(item['total_price']) for item in cart.values())

    if 'success_message' in request.session:
        messages.success(request, request.session['success_message'])
        del request.session['success_message']

    return render(request, 'cart.html', {'cart_items': cart, 'total_price': int(total_price)})

@login_required
def add_to_cart(request, product_id):
    if request.method == "POST":
        product = S_product.objects.get(id=product_id)
        quantity = int(request.POST.get("quantity", 1))  
        cart = request.session.get('cart', {})

        if str(product.id) in cart:
            cart[str(product.id)]['quantity'] += quantity
            # Recalculate total price for the updated quantity
            cart[str(product.id)]['total_price'] = str(float(cart[str(product.id)]['price']) * cart[str(product.id)]['quantity'])
        else:
            # Otherwise, add the product with its details to the cart
            cart[str(product.id)] = {
                'product_name': product.product_name,
                'price': str(product.price),  # Store price as a string to avoid Decimal issues
                'quantity': quantity,
                'total_price': str(float(product.price) * quantity)  # Total price is also stored as a string
            }
        # Update the session with the new cart
        request.session['cart'] = cart
        messages.success(request, f"{product.product_name} Telah ditambahkan ke keranjang.")

    return redirect('cart_page')

@login_required
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        messages.success(request, "Menghapus item dari keranjang sukses.")
    else:
        messages.error(request, "Item tidak dapat ditemukan di keranjang.")

    request.session['cart'] = cart
    return redirect('cart_page')

@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    products = []
    subtotal = Decimal(0)
    shipping_cost = Decimal(10)  # Optional, you can set this to 0 if shipping is not needed.
    total = Decimal(0)

    # Calculate cart subtotal and collect product details
    for product_id, product_details in cart.items():
        try:
            quantity = product_details.get('quantity', 1)
            s_product = S_product.objects.get(id=product_id)
            product_total = s_product.price * Decimal(quantity)
            subtotal += product_total
            products.append({
                'product': s_product,
                'quantity': quantity,
                'total_price': product_total
            })
        except S_product.DoesNotExist:
            continue

    total = subtotal + shipping_cost

    if request.method == 'POST':
        billing_form = BillingAddressForm(request.POST)
        payment_form = PaymentMethodForm(request.POST)

        if billing_form.is_valid() and payment_form.is_valid():
            # Logic for order processing can go here
            request.session['cart'] = {}  # Clear the cart
            messages.success(request, "Pesanan kamu sukses dibuat!")
            return redirect('terima_kasih')
        else:
            messages.error(request, "Terjadi kesalahan pada pengiriman formulir Anda. Silakan coba lagi.")
    else:
        billing_form = BillingAddressForm()
        payment_form = PaymentMethodForm()

    return render(request, 'checkout.html', {
        'products': products,
        'subtotal': subtotal,
        'shipping_cost': shipping_cost,
        'total': total,
        'billing_form': billing_form,
        'payment_form': payment_form,
    })

def thank_you(request):
    return render(request, 'thank_you.html', {'title': 'Thank You'})
    
def signup(request):
    if request.method == "POST":
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirmpassword')

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.info(request, 'Nama pengguna sudah dipakai')
            return redirect('signup')

        # Check if email already exists
        elif User.objects.filter(email=email).exists():
            messages.info(request, 'Email sudah dipakai')
            return redirect('signup')

        # Check if passwords match
        elif password != confirmpassword:
            messages.error(request, 'Kata sandi tidak cocok')
            return redirect('signup')

        else:
            # Create the user
            user = User.objects.create_user(username=username, email=email, password=password)
            user.first_name = fname
            user.last_name = lname
            user.save()
            messages.success(request, 'Pendaftaran berhasil! Silakan masuk.')
            return redirect('signin')

    else:
        return render(request, 'signup.html')

def signin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Log the user in
            auth_login(request, user)
            return redirect('index')  # Redirect to the home page or any other page
        else:
            messages.error(request, "Nama pengguna atau kata sandi tidak valid. Silakan coba lagi.")
            return redirect('signin')

    return render(request, 'signin.html')  # Correct indentation for the `else`

def logout(request):
    auth_logout(request)  # Logs out the user
    messages.success(request, "Anda telah berhasil keluar.")
    return redirect('signin')  # Redirect to the login page or another page