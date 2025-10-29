from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
class CustomUser(AbstractUser):
    class Types(models.TextChoices):
        HR = "hr", "HR"
        EMPLOYEE = "employee", "Employee"

    type = models.CharField(max_length=20, choices=Types.choices)
    groups = models.ManyToManyField(Group, related_name="custom_user_groups1", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="custom_user_permissions1", blank=True)
    def __str__(self):
        return self.username

