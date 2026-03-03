from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Order, OrderItem
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout

def custom_logout(request):
    logout(request)
    return redirect('product_list')

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # after registration, go to login
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def product_list(request):
    products = Product.objects.all()
    return render(request, 'shop/product_list.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'shop/product_detail.html', {'product': product})



def add_to_cart(request, pk):
    cart = request.session.get('cart', {})
    cart[str(pk)] = cart.get(str(pk), 0) + 1
    request.session['cart'] = cart
    return redirect('cart_detail')

def cart_detail(request):
    cart = request.session.get('cart', {})
    products = []
    total = 0
    for pk, quantity in cart.items():
        product = get_object_or_404(Product, pk=pk)
        products.append({'product': product, 'quantity': quantity})
        total += product.price * quantity
    return render(request, 'shop/cart_detail.html', {'products': products, 'total': total})


@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('cart_detail')

    order = Order.objects.create(user=request.user)

    for pk, quantity in cart.items():
        product = get_object_or_404(Product, pk=pk)
        OrderItem.objects.create(order=order, product=product, quantity=quantity)

    request.session['cart'] = {}

    return render(request, 'shop/checkout_success.html', {'order': order})
