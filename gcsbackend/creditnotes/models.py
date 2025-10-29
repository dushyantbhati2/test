from django.db import models
from uuid import uuid4
from customer.models import Customer
# Create your models here.
class CreditNote(models.Model):
    id=models.UUIDField(default=uuid4,primary_key=True,editable=False)
    note_number=models.PositiveIntegerField()
    date=models.DateField()
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE,null=True,blank=True)
    reference=models.CharField(max_length=255)
    reason=models.TextField()
    notes=models.TextField(blank=True)

    