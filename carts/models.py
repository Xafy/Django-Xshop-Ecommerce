from django.db.models.deletion import CASCADE
from django.db.models.signals import m2m_changed, pre_save, post_save
from products.models import Product
from django.contrib.auth.models import User
from django.db import models

from django.conf import settings
User = settings.AUTH_USER_MODEL

class CartManager(models.Manager):

    def new_or_get(self, request):
        cart_id = request.session.get('cart_id', None)
        qs = self.get_queryset().filter(id=cart_id)
        if qs.count() == 1:
            new_obj = False
            cart_obj = qs.first()
            if request.user.is_authenticated and cart_obj.user is None:
                cart_obj.user = request.user
                cart_obj.save()
        else:
            new_obj = True
            cart_obj = Cart.objects.new(user=None)
            request.session['cart_id'] = cart_obj.id

        return cart_obj, new_obj

    def new(self, user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated():
                user_obj = user
        return self.model.objects.create(user = user_obj)

class Cart(models.Model):
    user            = models.ForeignKey(User, blank=True, null=True, on_delete=CASCADE)
    products        = models.ManyToManyField(Product, blank=True)
    sub_total       = models.FloatField(default=00.00, max_length=20)
    total           = models.FloatField(default=00.00, max_length=20)
    timestamp       = models.DateTimeField(auto_now_add=True)
    updated         = models.DateTimeField(auto_now=True)

    objects = CartManager()

    def __str__(self):
        return str(self.id)

def m2m_changed_cart_reciever(sender, instance, action, *args, **kwargs):
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        products = instance.products.all()
        sub_total = 0
        for x in products:
            sub_total += x.price
        instance.sub_total = sub_total
        instance.save()

m2m_changed.connect(m2m_changed_cart_reciever, sender = Cart.products.through)

def pre_save_cart_reciever(sender, instance, *args, **kwargs):
    instance.total = instance.sub_total * 1.25

pre_save.connect(pre_save_cart_reciever, sender = Cart)