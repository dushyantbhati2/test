
# inquiry/tests.py
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from user.models import CustomUser
from employee.models import Employee
from .models import Inquiry
from rest_framework_simplejwt.tokens import RefreshToken
from employee.models import Department
class InquiryAPITest(TestCase):
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
			department_id=self.department.id,
			employment_type="Full-time",
			basic_salary=1000,
			hourly_rate=10,
			phone_number="1234567890",
			address="Test Address"
		)
		self.inquiry = Inquiry.objects.create(
			subject="Test Inquiry",
			requirements="Test requirements",
			source="Email",
			status="Open",
			budget=1000,
			timeline="1 month",
			assigned_to=self.employee,
			follow_up_date="2025-01-01"
		)

	def test_list_inquiries(self):
		response = self.client.get("/inquiry/")
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_retrieve_inquiry(self):
		response = self.client.get(f"/inquiry/{self.inquiry.id}/")
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_create_inquiry(self):
		data = {
			"subject": "New Inquiry",
			"requirements": "New requirements",
			"source": "Phone",
			"status": "Pending",
			"budget": 2000,
			"timeline": "2 months",
			"assigned_to": str(self.employee.id),
			"follow_up_date": "2025-02-01"
		}
		response = self.client.post("/inquiry/", data, format="json")
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

	def test_update_inquiry(self):
		data = {
			"subject": "Updated Inquiry",
			"requirements": "Updated requirements",
			"source": "Web",
			"status": "Closed",
			"budget": 1500,
			"timeline": "3 months",
			"assigned_to": str(self.employee.id),
			"follow_up_date": "2025-03-01"
		}
		response = self.client.put(f"/inquiry/{self.inquiry.id}/", data, format="json")
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data["subject"], "Updated Inquiry")

	def test_delete_inquiry(self):
		response = self.client.delete(f"/inquiry/{self.inquiry.id}/")
		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
		self.assertFalse(Inquiry.objects.filter(id=self.inquiry.id).exists())
