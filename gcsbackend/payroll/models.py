from django.db import models
from employee.models import Employee
from uuid import uuid4
from utils.pay_period import current_month_period
class Payroll(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid4, editable=False)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2)
    pay_month=models.CharField(max_length=20,default=current_month_period)
    transaction_id=models.CharField(max_length=100,default=uuid4)
    allowances = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=50, default="pending")
    notes=models.TextField(blank=True)

    def __str__(self):
        return f"Payroll for {self.employee.name} on {self.date}"
    
    @property
    def net_salary(self):
        return self.basic_salary + self.allowances - self.deductions
