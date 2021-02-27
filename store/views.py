from django.shortcuts import render
from .models import *

# Create your views here.

def index(request):
    context = {}
    return render(request, 'store/index.html', context)

def cart(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}

    context = {'items': items, 'order': order}
    return render(request, 'store/cart.html', context)

def shop(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'store/shop.html', context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
        
    context = {'items': items, 'order': order}
    return render(request, 'store/checkout.html', context)

def blog(request):
    context = {}
    return render(request, 'store/blog.html', context)

def faq(request):
    context = {}
    return render(request, 'store/faq.html', context)

def contact(request):
    context = {}
    return render(request, 'store/contact.html', context)
