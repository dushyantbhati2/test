from rest_framework import serializers
from django.shortcuts import get_object_or_404
from django.db import transaction
from . import models

class EmployeeSerializer(serializers.ModelSerializer):
    managers = serializers.SerializerMethodField()
    department = serializers.CharField(write_only=True)  # take department name
    department_name = serializers.CharField(source="department.name", read_only=True)
    manager = serializers.UUIDField(write_only=True, required=False, allow_null=True)  # optional

    class Meta:
        model = models.Employee
        fields = "__all__"

    @transaction.atomic
    def create(self, validated_data):
        department_name = validated_data.pop("department")
        manager_id = validated_data.pop("manager", None)

        # get or create department by name
        department, _ = models.Department.objects.get_or_create(name=department_name)
        employee = models.Employee.objects.create(department=department, **validated_data)

        # link manager if provided
        if manager_id:
            manager = get_object_or_404(models.Employee, id=manager_id)
            models.Manager.objects.create(manager=manager, employee=employee)

        return employee

    @transaction.atomic
    def update(self, instance, validated_data):
        department_name = validated_data.pop("department", None)
        if department_name:
            department, _ = models.Department.objects.get_or_create(name=department_name)
            instance.department = department

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

    def get_managers(self, obj):
        manager_links = models.Manager.objects.filter(employee=obj).select_related("manager")
        return [
            {
                "id": m.manager.id,
                "name": m.manager.name,
                "email": m.manager.email,
                "job_title": m.manager.job_title,
            }
            for m in manager_links
        ]


class ManagerSerializer(serializers.ModelSerializer):
    manager = EmployeeSerializer(read_only=True)
    employee = EmployeeSerializer(read_only=True)

    class Meta:
        model = models.Manager
        fields = "__all__"
