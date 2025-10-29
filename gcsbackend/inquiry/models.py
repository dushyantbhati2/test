from django.db import models
from uuid import uuid4
from employee.models import Employee
# Create your models here.
class Inquiry(models.Model):
    id=models.UUIDField(default=uuid4,primary_key=True,editable=False)
    date=models.DateField(auto_now_add=True)
    subject=models.CharField(max_length=255)
    requirements=models.TextField()
    source=models.CharField(max_length=255)
    status=models.CharField(max_length=255)
    budget=models.IntegerField(blank=True)
    timeline=models.CharField(max_length=255)
    assigned_to=models.ForeignKey(Employee,on_delete=models.CASCADE)
    follow_up_date=models.DateField()
    notes=models.TextField(blank=True)
# lsa, fcp,gmdss(communication),ga