from django.db import models
from uuid import uuid4

class Customer(models.Model):
    id=models.UUIDField(default=uuid4,primary_key=True,editable=False)
    customer_type = models.CharField(max_length=50)
    company_name = models.CharField(max_length=255)
    gst_number = models.CharField(max_length=15)
    pan_number = models.CharField(max_length=10)
    gst_state = models.CharField(max_length=100) 
    gst_type = models.CharField(max_length=50)
    credit_terms_days = models.PositiveIntegerField()
    credit_limit = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.company_name if self.company_name else f"Customer {self.id}"


class Contact(models.Model):
    id=models.UUIDField(default=uuid4,primary_key=True,editable=False)
    customer = models.ForeignKey(Customer, related_name="contacts", on_delete=models.CASCADE)
    title = models.CharField(max_length=10, blank=True, null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    designation = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    alternate_phone = models.CharField(max_length=20, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name or ''}".strip()


class Address(models.Model):
    id=models.UUIDField(default=uuid4,primary_key=True,editable=False)
    customer = models.ForeignKey(Customer, related_name="addresses", on_delete=models.CASCADE)
    address_type = models.CharField(max_length=100)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=100, default="India")
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.address_type.title()} Address - {self.customer}"
