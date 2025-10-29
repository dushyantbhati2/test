from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.Quotation)
admin.site.register(models.QuotationItem)