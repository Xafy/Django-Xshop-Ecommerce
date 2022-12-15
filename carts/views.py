from accounts.models import GuestEmail
from orders.models import Order
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect
from accounts.forms import SigninForm, GuestForm
# from accounts.models import GuestEmail
from billing.models import BillingProfile

from addresses.forms import AddressForm
from addresses.models import Address

# from orders.models import Order
from products.models import Product
from .models import Cart

User = settings.AUTH_USER_MODEL

def cart_detail_api_view(request):
     cart_obj, new_obj = Cart.objects.new_or_get(request) 
     products = [
         {
            "id" : x.id,
            "url" : x.get_absolute_url(),
            "title" : x.title,
            "price" : x.price
        }
        for x in cart_obj.products.all()]
     cart_data = {"products" : products, "subtotal" : cart_obj.sub_total, "total" : cart_obj.total}
     return JsonResponse(cart_data)

def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    return render(request, "carts/home.html", {'cart' : cart_obj})

def cart_update(request):
    product_id = request.POST.get('product_id')
    if product_id is not None:
        try:
            product_obj = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            print("show message to user, product is gone")
            return redirect("cart:home")
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        if product_obj in cart_obj.products.all():
            cart_obj.products.remove(product_obj)
            added = False
        else:
            cart_obj.products.add(product_obj)
            added = True
        request.session['cart_items'] = cart_obj.products.count()
        if request.is_ajax():
            json_data = {
                "added" : added,
                "removed" : not added,
                "cartCount" : cart_obj.products.count(),
            }
            return JsonResponse(json_data)
    return redirect("cart:home")

def checkout_home(request):
    login_form = SigninForm()
    guest_form = GuestForm() 
    address_form = AddressForm
    billing_address_form = AddressForm
    
    order_obj = None
    billing_address_id = request.session.get("billing_address_id", None)
    shipping_address_id = request.session.get("shipping_address_id", None)
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    if cart_created or cart_obj.products.count() == 0:
        return redirect("cart:home")

    billing_profile , billing_profile_created = BillingProfile.objects.new_or_get(request)
    address_qs = None
    if billing_profile is not None:
        if request.user.is_authenticated:
            address_qs = Address.objects.filter(billing_profile=billing_profile)
        order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
        if billing_address_id :
            order_obj.billing_address = Address.objects.get(id = billing_address_id)
            del request.session['billing_address_id']
        if shipping_address_id :
            order_obj.shipping_address = Address.objects.get(id = shipping_address_id)
            del request.session['shipping_address_id']
        if billing_address_id or shipping_address_id:
            order_obj.save()

    if request.method == "POST":
        is_done = order_obj.checkout_done()
        if is_done :
            order_obj.mark_paid()
            del request.session['cart_id']
            request.session['cart_items'] = 0
            return redirect("cart:done")

    context = {
        "object" : order_obj,
        "billing_profile" : billing_profile,
        "login_form" : login_form,
        "guest_form" : guest_form,
        "address_form" : address_form,
        "billing_address_form" : billing_address_form,
        "address_qs" : address_qs
    }
    return render(request, "carts/checkout.html", context)

def checkout_done(request):
    return render(request, "carts/checkout-done.html", {})