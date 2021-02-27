from django.shortcuts import render

# Create your views here.

def index(request):
    context = {}
    return render(request, 'store/index.html', context)

def cart(request):
    context = {}
    return render(request, 'store/cart.html', context)

def shop(request):
    context = {}
    return render(request, 'store/shop.html', context)

def checkout(request):
    context = {}
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
