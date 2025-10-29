from django.db import models
from uuid import uuid4
from customer.models import Customer

class Vessel(models.Model):
    id=models.UUIDField(default=uuid4,primary_key=True,editable=False)
    name=models.CharField(max_length=255)
    imo_number=models.CharField(max_length=255)
    type=models.CharField(max_length=255)
    owner=models.ForeignKey(Customer,on_delete=models.CASCADE)
    flag_state=models.CharField(max_length=255,blank=True, null=True)
    classification_society=models.CharField(max_length=255,blank=True, null=True)
    class_notation=models.CharField(max_length=255,blank=True, null=True)
    build_year=models.PositiveIntegerField(blank=True, null=True)
    shipyard=models.CharField(max_length=255,blank=True, null=True)
    length_overall = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    breadth = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    depth = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    gross_tonnage = models.PositiveIntegerField(blank=True, null=True)
    net_tonnage = models.PositiveIntegerField(blank=True, null=True)
    deadweight = models.PositiveIntegerField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Test(models.Model):
    id=models.UUIDField(default=uuid4,primary_key=True,editable=False)
    name=models.CharField(max_length=255,blank=True)
    def __str__(self):
        return self.name