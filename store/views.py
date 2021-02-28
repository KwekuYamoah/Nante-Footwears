from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from .models import *
import json
import datetime
from . utils import cookieCart, cartData, guestOrder
from pypaystack import Transaction, Customer, Plan

# Create your views here.

def index(request):

    data = cartData(request)
    cartItems = data['cartItems']

    context = {'cartItems': cartItems}
    return render(request, 'store/index.html', context)

def cart(request):

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)

def shop(request):

    data = cartData(request)
    cartItems = data['cartItems']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/shop.html', context)

def checkout(request):

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
        
    context = {'items': items, 'order': order, 'cartItems': cartItems, "pk_public" : settings.PAYSTACK_PUBLIC_KEY}
    return render(request, 'store/checkout.html', context)

def blog(request):

    data = cartData(request)
    cartItems = data['cartItems']

    context = {'cartItems': cartItems}
    return render(request, 'store/blog.html', context)

def faq(request):

    data = cartData(request)
    cartItems = data['cartItems']

    context = {'cartItems': cartItems}
    return render(request, 'store/faq.html', context)

def contact(request):

    data = cartData(request)
    cartItems = data['cartItems']

    context = {'cartItems': cartItems}
    return render(request, 'store/contact.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item added', safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

        DeliveryAddress.objects.create(
            customer = customer,
            order = order,
            address = data['shipping']['street'],
            city = data['shipping']['town']
        )
    else:
        print('User not logged in')
        print('COOKIES:', request.COOKIES)
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    return JsonResponse('Payment Confirmed', safe=False)

def verify(request, id):
    transaction = Transaction(authorization_key=settings.PAYSTACK_SECRET_KEY)
    response = transaction.verify(id)
    data = JsonResponse(response, safe=False)
    return data