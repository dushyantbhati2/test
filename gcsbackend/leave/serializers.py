from rest_framework import serializers
from . import models

class LeaveRequestSerializer(serializers.ModelSerializer):
    employee = serializers.SerializerMethodField(read_only=True)
    employee_id = serializers.PrimaryKeyRelatedField(queryset=models.Employee.objects.all(),source='employee',write_only=True)

    class Meta:
        model = models.LeaveRequest
        fields = "__all__"

    def get_employee(self, obj):
        return {
            "name": obj.employee.name,
            "job_title": obj.employee.job_title,
        }
