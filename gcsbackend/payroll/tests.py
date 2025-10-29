
# payroll/tests.py
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from user.models import CustomUser
from employee.models import Employee
from .models import Payroll
from rest_framework_simplejwt.tokens import RefreshToken
from employee.models import Department
class PayrollAPITest(TestCase):
	def setUp(self):
		self.client = APIClient()
		self.user = CustomUser.objects.create_user(
			username="testuser",
			password="testpass",
			type="hr"
		)
		refresh = RefreshToken.for_user(self.user)
		self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
		self.department=Department.objects.create(name="Engineering")
		self.employee = Employee.objects.create(
			name="Test Employee",
			email="employee@example.com",
			job_title="Engineer",
			department_id=self.department.id,
			employment_type="Full-time",
			basic_salary=1000,
			hourly_rate=10,
			phone_number="1234567890",
			address="Test Address"
		)
		self.payroll = Payroll.objects.create(
			employee=self.employee,
			basic_salary=1000,
			allowances=100,
			deductions=50,
			status="pending"
		)

	def test_list_payrolls(self):
		response = self.client.get("/payroll/")
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_retrieve_payroll(self):
		response = self.client.get(f"/payroll/{self.payroll.id}/")
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_create_payroll(self):
		data = {
			"employee": str(self.employee.id),
			"basic_salary": 2000,
			"allowances": 200,
			"deductions": 100,
			"status": "approved"
		}
		response = self.client.post("/payroll/", data, format="json")
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

	def test_update_payroll(self):
		data = {
			"employee": str(self.employee.id),
			"basic_salary": 1500,
			"allowances": 150,
			"deductions": 75,
			"status": "approved"
		}
		response = self.client.patch(f"/payroll/{self.payroll.id}/", data, format="json")
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data["status"], "approved")

	def test_delete_payroll(self):
		response = self.client.delete(f"/payroll/{self.payroll.id}/")
		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
		self.assertFalse(Payroll.objects.filter(id=self.payroll.id).exists())
