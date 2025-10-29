from django.db import models
from employee.models import Employee
from uuid import uuid4

class Attendance(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid4, editable=False)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    check_in = models.TimeField(auto_now_add=True)
    check_out = models.TimeField(auto_now_add=True)
    status = models.CharField(max_length=50)
    notes=models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Attendance for {self.employee.name} on {self.date}"