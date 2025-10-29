from django.db import models
from uuid import uuid4
from projects.models import Project

# Create your models here.

class Requirement(models.Model):
    id=models.UUIDField(default=uuid4,primary_key=True,editable=False)
    title=models.CharField(max_length=255)
    project=models.ForeignKey(Project,on_delete=models.CASCADE)
    description=models.TextField(blank=True)
    type=models.CharField(max_length=255)
    priority=models.CharField(max_length=255)
    status=models.CharField(max_length=255)

    def __str__(self):
        return f'{self.title} for {self.project.name}'