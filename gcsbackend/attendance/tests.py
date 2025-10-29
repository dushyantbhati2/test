# attendance/tests.py
import uuid
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from employee.models import Employee
from .models import Attendance
from django.contrib.auth import get_user_model 
from employee.models import Department

class AttendanceAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        User = get_user_model()
        self.user = User.objects.create_user(
            username="testuser", password="testpass", type="hr"
        )
        self.client.force_authenticate(user=self.user)  
        self.department = Department.objects.create(id=uuid.uuid4(), name="Engineering")

        self.employee = Employee.objects.create(
            id=uuid.uuid4(),
            name="John Doe",
            email="john@example.com",
            job_title="Engineer",
            department=self.department,
            employment_type="Full-time",
            basic_salary=50000,
            hourly_rate=500,
            phone_number="1234567890",
            address="Test Address"
        )

        self.attendance = Attendance.objects.create(
            employee=self.employee,
            status="Present",
            notes="On time"
        )

    def test_list_attendance(self):
        """GET /attendance/"""
        response = self.client.get("/attendance/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_retrieve_attendance(self):
        """GET /attendance/{id}/"""
        response = self.client.get(f"/attendance/{self.attendance.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], str(self.attendance.id))

    def test_create_attendance(self):
        """POST /attendance/"""
        data = {
            "employee": str(self.employee.id),
            "status": "Absent",
            "notes": "Sick leave"
        }
        response = self.client.post("/attendance/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["status"], "Absent")

    def test_update_attendance(self):
        """PUT /attendance/{id}/"""
        data = {
            "employee": str(self.employee.id),
            "status": "Late",
            "notes": "Arrived late"
        }
        response = self.client.put(f"/attendance/{self.attendance.id}/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "Late")

    def test_delete_attendance(self):
        """DELETE /attendance/{id}/"""
        response = self.client.delete(f"/attendance/{self.attendance.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["success"], "Attendance record deleted")
