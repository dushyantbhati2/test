from rest_framework import serializers
from .models import Payroll

class PayrollSerializer(serializers.ModelSerializer):
    net_salary = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Payroll
        fields = ["id", "employee", "date", "basic_salary", "allowances", "deductions",
                  "net_salary", "status", "notes","pay_month","transaction_id"]
        
    

