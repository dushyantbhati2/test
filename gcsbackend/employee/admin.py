from django.contrib import admin
from . import models

admin.site.register(models.Department)
admin.site.register(models.Manager)
admin.site.register(models.Employee)
