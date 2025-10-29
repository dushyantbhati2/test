from django.db import models
from uuid import uuid4
from employee.models import Employee
from projects.models import Project


class Task(models.Model):
    id=models.UUIDField(default=uuid4,primary_key=True,editable=False)
    project=models.ForeignKey(Project,on_delete=models.CASCADE)
    project_phase=models.CharField(max_length=255,blank=True)
    title=models.CharField(max_length=255)
    description=models.TextField(blank=True)
    type=models.CharField(max_length=255,blank=True)
    plan_type=models.CharField(max_length=255,blank=True)
    plan_number=models.CharField(max_length=255)
    revision=models.CharField(max_length=255,default='A')
    assigned_to=models.ForeignKey(Employee,on_delete=models.CASCADE)
    due_date=models.DateField()
    status=models.CharField(max_length=255)
    priority=models.CharField(max_length=255)
    estimated_hours=models.PositiveIntegerField()
    completion=models.PositiveIntegerField()
    regulatory_approval=models.BooleanField(default=False)
    dependencies=models.TextField(blank=True)
    notes=models.TextField(blank=True)

    def __str__(self):
        return self.title


