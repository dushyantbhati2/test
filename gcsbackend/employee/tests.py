
# employee/tests.py
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from user.models import CustomUser
from .models import Employee, Department
from rest_framework_simplejwt.tokens import RefreshToken

class EmployeeAPITest(TestCase):
	def setUp(self):
		self.client = APIClient()
		self.user = CustomUser.objects.create_user(
			username="testuser",
			password="testpass",
			type="hr"
		)
		refresh = RefreshToken.for_user(self.user)
		self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
		self.department = Department.objects.create(name="Engineering")
		self.employee = Employee.objects.create(
			name="Test Employee",
			email="employee@example.com",
			job_title="Engineer",
			department=self.department,
			employment_type="Full-time",
			basic_salary=1000,
			hourly_rate=10,
			phone_number="1234567890",
			address="Test Address"
		)
	
	def test_list_employees(self):
		response = self.client.get("/employee/")
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_retrieve_employee(self):
		response = self.client.get(f"/employee/{self.employee.id}/")
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_create_employee(self):
		data = {
			"name": "New Employee",
			"email": "newemployee@example.com",
			"job_title": "Manager",
			"department": str(self.department.id),
			"employment_type": "Part-time",
			"basic_salary": 2000,
			"hourly_rate": 20,
			"phone_number": "9876543210",
			"address": "New Address"
		}
		response = self.client.post("/employee/", data, format="json")
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

	def test_update_employee(self):
		data = {
			"name": "Updated Employee",
			"email": "employee@example.com",
			"job_title": "Lead Engineer",
			"department": str(self.department.id),
			"employment_type": "Full-time",
			"basic_salary": 1500,
			"hourly_rate": 15,
			"phone_number": "1234567890",
			"address": "Updated Address"
		}
		response = self.client.patch(f"/employee/{self.employee.id}/", data, format="json")
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data["name"], "Updated Employee")

	def test_delete_employee(self):
		response = self.client.delete(f"/employee/{self.employee.id}/")
		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
		self.assertFalse(Employee.objects.filter(id=self.employee.id).exists())
