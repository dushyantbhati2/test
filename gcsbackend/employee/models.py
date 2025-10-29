from django.db import models
from uuid import uuid4
class Department(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name=models.CharField(max_length=100,unique=True)
    def __str__(self):
        return self.name

class Employee(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    job_title=models.CharField(max_length=100)
    department=models.ForeignKey(Department,on_delete=models.CASCADE)
    employment_type=models.CharField(max_length=100)
    basic_salary=models.DecimalField(max_digits=10, decimal_places=2)
    hourly_rate=models.DecimalField(max_digits=10, decimal_places=2)
    phone_number=models.CharField(max_length=15)
    address=models.TextField()
    date_of_joining=models.DateField(auto_now_add=True)
    status=models.CharField(max_length=50,default="active")
    def __str__(self):
        return f"{self.name}"
 
class Manager(models.Model):
    manager=models.ForeignKey(Employee,on_delete=models.CASCADE,related_name='manager')
    employee=models.ForeignKey(Employee,on_delete=models.CASCADE,related_name='employees')
    def __str__(self):
        return f"{self.manager.name} - Manager manages {self.employee.name} employees"
