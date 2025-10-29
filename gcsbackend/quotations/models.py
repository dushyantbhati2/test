from django.db import models
from uuid import uuid4
from customer.models import Customer
from vessels.models import Vessel

class Quotation(models.Model):
    id=models.UUIDField(default=uuid4,primary_key=True,editable=False)
    quotation_number = models.CharField(max_length=50, unique=True)
    date = models.DateField()
    valid_until = models.DateField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="quotations")
    project = models.CharField(max_length=255)
    vessel = models.ForeignKey(Vessel, on_delete=models.CASCADE)
    place_of_supply = models.CharField(max_length=255)
    design_scope = models.TextField(blank=True, null=True)
    delivery_location = models.CharField(max_length=255, blank=True, null=True)
    revision_rounds = models.PositiveIntegerField(default=1)
    notes = models.TextField(blank=True, null=True)
    terms_and_conditions = models.TextField(blank=True, null=True)

class QuotationItem(models.Model):
    id=models.UUIDField(default=uuid4,primary_key=True,editable=False)
    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE, related_name="items")
    description = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    tax_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    plan_type = models.CharField(max_length=100, blank=True, null=True)
    delivery_days = models.PositiveIntegerField()