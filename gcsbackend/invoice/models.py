from django.db import models
from uuid import uuid4
from customer.models import Customer
from projects.models import Project
from vessels.models import Vessel


class Invoice(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, editable=False)
    invoice_no = models.CharField(max_length=20, unique=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="invoices")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="invoices", null=True, blank=True)
    vessel = models.ForeignKey(Vessel, on_delete=models.CASCADE, related_name="invoices", null=True, blank=True)
    invoice_date = models.DateField()
    due_date = models.DateField()
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, default="Draft")
    place_of_supply = models.CharField(max_length=255)
    po_no=models.CharField(max_length=100, blank=True, null=True)
    our_ref=models.CharField(max_length=100, blank=True, null=True)
    sgst = models.DecimalField(max_digits=10, decimal_places=2, default=9.00)
    cgst = models.DecimalField(max_digits=10, decimal_places=2, default=9.00)
    igst = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
        if not self.invoice_no:
            last_invoice = Invoice.objects.order_by("id").last()
            if last_invoice:
                last_no = int(last_invoice.invoice_no.split("-")[-1])
                self.invoice_no = f"INV-{last_no + 1:04d}"
            else:
                self.invoice_no = "INV-0001"
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"Invoice {self.invoice_no} - {self.customer}"


class InvoiceItem(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, editable=False)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="items")
    description = models.TextField()
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    amount = models.DecimalField(max_digits=12, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        self.amount = self.quantity * self.unit_price
        super().save(*args, **kwargs)
        self.invoice.total_amount = sum(item.amount for item in self.invoice.items.all())
        self.invoice.save()

    def __str__(self):
        return f"{self.description} ({self.quantity} x {self.unit_price})"
