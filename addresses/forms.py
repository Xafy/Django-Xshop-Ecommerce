from django import forms
from django.db.models import fields

from .models import Address

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            'address_line_1',
            'address_line_2',
            'country',
            'city',
            'state',
            'postal_code',
        ]