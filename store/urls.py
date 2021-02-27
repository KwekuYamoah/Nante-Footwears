from django.urls import path
from . import views

urlpatterns = [

    path('', views.index, name="home"),
    path('shop/', views.shop, name="shop"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('blog/', views.blog, name="blog"),
    path('faq/', views.faq, name="faq"),
    path('contact/', views.contact, name="contact"),
]