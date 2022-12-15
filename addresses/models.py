from django.db import models
from django.db.models.deletion import CASCADE
from billing.models import BillingProfile

# Create your models here.
ADDRESS_TYPES = (
    ('billing', 'Billing'),
    ('shipping', 'Shipping')
)

class Address(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, on_delete = CASCADE)
    address_type    = models.CharField(max_length=40, choices=ADDRESS_TYPES)
    address_line_1  = models.CharField(max_length=140)
    address_line_2  = models.CharField(max_length=140, null=True, blank=True)
    country         = models.CharField(max_length=50)
    city            = models.CharField(max_length=50)
    state           = models.CharField(max_length=50)
    postal_code     = models.CharField(max_length=20) 

    def __str__(self):
        return str(self.billing_profile)

    def get_address(self):
        return "{line1}\n{line2}\n{city}\n{state}-{postal}\n{country}".format(
            line1 = self.address_line_1,
            line2 = self.address_line_2 or '',
            country = self.country,
            city = self.city,
            state = self.state,
            postal = self.postal_code,
        )
    