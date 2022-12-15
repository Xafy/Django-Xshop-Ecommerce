"""Xshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from carts.views import cart_home
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView

from django.contrib import admin
from django.urls import path, include

# from products.views import (ProductListView,
#                             product_list_view,
#                             ProductDetailView,
#                             product_detail_view,
#                             ProductFeaturedListView,
#                             ProductFeaturedDetailView,)
from addresses.views import checkout_address_create_view, checkout_address_reuse_view
from accounts.views import SigninView, SignupView, guest_signup_view
from carts.views import cart_detail_api_view
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_page, name = 'home'),
    path('contact/', views.contact_page, name = 'contact'),
    path('signin/', SigninView.as_view(), name = 'signin'),
    path('signup/guest/', guest_signup_view, name = 'guest_signup'),
    path('signup/', SignupView.as_view(), name = 'signup'),
    path('logout/', LogoutView.as_view(), name = 'logout'),
    path('products/', include(('products.urls', 'products'), namespace='products')),
    path('cart/', include(('carts.urls', 'carts'), namespace='cart')),
    path('api/cart/', cart_detail_api_view, name='api-cart'),
    path('checkout/address/create/', checkout_address_create_view, name = 'checkout_address_create'),
    path('checkout/address/reuse/', checkout_address_reuse_view, name = 'checkout_address_reuse'),
    # path('products-fbv/', product_list_view),
    # path('products/<pk>', ProductDetailView.as_view()),
    # path('products-fbv/<pk>', product_detail_view),
    # path('featured/', ProductFeaturedListView.as_view()),
    # path('featured/<pk>', ProductFeaturedDetailView.as_view()),

]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
