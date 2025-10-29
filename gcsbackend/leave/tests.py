
# leave/tests.py
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from user.models import CustomUser
from employee.models import Employee
from .models import LeaveRequest
from rest_framework_simplejwt.tokens import RefreshToken
from employee.models import Department
class LeaveRequestAPITest(TestCase):
	def setUp(self):
		self.client = APIClient()
		self.user = CustomUser.objects.create_user(
			username="testuser",
			password="testpass",
			type="hr"
		)
		refresh = RefreshToken.for_user(self.user)
		self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
		self.department_id = Department.objects.create(name="HR").id
		self.employee = Employee.objects.create(
			name="Test Employee",
			email="employee@example.com",
			job_title="Engineer",
			department_id=self.department_id,
			employment_type="Full-time",
			basic_salary=1000,
			hourly_rate=10,
			phone_number="1234567890",
			address="Test Address"
		)
		self.leave = LeaveRequest.objects.create(
			employee=self.employee,
			start_date="2025-01-01",
			end_date="2025-01-05",
			reason="Vacation",
			contact="1234567890",
			emergency_contact="0987654321",
			type="Annual"
		)

	def test_list_leaves(self):
		response = self.client.get("/leave/")
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_retrieve_leave(self):
		response = self.client.get(f"/leave/{self.leave.id}/")
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_create_leave(self):
		data = {
			"employee": str(self.employee.id),
			"start_date": "2025-02-01",
			"end_date": "2025-02-03",
			"reason": "Medical",
			"contact": "1234567890",
			"emergency_contact": "0987654321",
			"type": "Sick"
		}
		response = self.client.post("/leave/", data, format="json")
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

	def test_update_leave(self):
		data = {
			"employee": str(self.employee.id),
			"start_date": "2025-01-01",
			"end_date": "2025-01-05",
			"reason": "Updated Reason",
			"contact": "1234567890",
			"emergency_contact": "0987654321",
			"type": "Annual"
		}
		response = self.client.put(f"/leave/{self.leave.id}/", data, format="json")
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data["reason"], "Updated Reason")

	def test_delete_leave(self):
		response = self.client.delete(f"/leave/{self.leave.id}/")
		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
		self.assertFalse(LeaveRequest.objects.filter(id=self.leave.id).exists())
