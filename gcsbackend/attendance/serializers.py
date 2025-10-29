from rest_framework import serializers
from . import models
from employee.models import Employee
from employee.serializers import EmployeeSerializer  # Import your Employee serializer

class AttendanceSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(read_only=True)  # Serialize full employee object
    employee_id = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(), source='employee', write_only=True
    )

    class Meta:
        model = models.Attendance
        fields = "__all__"

    def create(self, validated_data):
        return models.Attendance.objects.create(**validated_data)
