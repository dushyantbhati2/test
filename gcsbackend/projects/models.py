from django.db import models
from uuid import uuid4
from vessels.models import Customer
from employee.models import Employee

class Project(models.Model):
    id=models.UUIDField(default=uuid4,primary_key=True,editable=False)
    name=models.CharField(max_length=255)
    type=models.CharField(max_length=255)
    description=models.TextField(blank=True)
    status=models.CharField(max_length=255)
    priority=models.CharField(max_length=255)
    design_phase=models.CharField(max_length=255)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    # vessel=models.ForeignKey(Vessel,on_delete=models.CASCADE)
    regulatory_body=models.CharField(max_length=255,blank=True)
    classification_society=models.CharField(max_length=255,blank=True)
    start_date=models.DateField()
    end_date=models.DateField()
    terms=models.TextField(blank=True)
    manager=models.ForeignKey(Employee,on_delete=models.CASCADE)
    notes=models.TextField(blank=True)
    budget=models.PositiveIntegerField(blank=True,null=True)
    value=models.PositiveIntegerField(blank=True,null=True)
    enable_payments=models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    