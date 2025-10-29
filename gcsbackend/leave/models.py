from django.db import models
from employee.models import Employee
import uuid
class LeaveRequest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    contact = models.CharField(max_length=100)
    emergency_contact = models.CharField(max_length=255,blank=True)
    type=models.CharField(max_length=100)   

    def __str__(self):
        return f"LeaveRequest for {self.employee.name} from {self.start_date} to {self.end_date}"