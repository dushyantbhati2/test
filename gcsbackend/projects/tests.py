
# projects/tests.py
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from user.models import CustomUser
from employee.models import Employee
from customer.models import Customer
from vessels.models import Vessel
from .models import Project
from rest_framework_simplejwt.tokens import RefreshToken
from employee.models import Department
class ProjectAPITest(TestCase):
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
		self.customer = Customer.objects.create(
			customer_type="Company",
			company_name="Test Customer",
			gst_number="22AAAAA0000A1Z5",
			pan_number="ABCDE1234F",
			gst_state="State",
			gst_type="Regular",
			credit_terms_days=30,
			credit_limit=10000.00
		)
		self.vessel = Vessel.objects.create(
			name="Test Vessel",
			imo_number="IMO1234567",
			type="Cargo",
			owner=self.customer
		)
		self.employee = Employee.objects.create(
			name="Test Manager",
			email="manager@example.com",
			job_title="Manager",
			department_id=self.department.id,
			employment_type="Full-time",
			basic_salary=2000,
			hourly_rate=20,
			phone_number="1234567890",
			address="Manager Address"
		)
		self.project = Project.objects.create(
			name="Test Project",
			type="Design",
			status="Active",
			priority="High",
			design_phase="Phase 1",
			customer=self.customer,
			vessel=self.vessel,
			start_date="2025-01-01",
			end_date="2025-12-31",
			manager=self.employee
		)

	def test_list_projects(self):
		response = self.client.get("/projects/")
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_retrieve_project(self):
		response = self.client.get(f"/projects/{self.project.id}/")
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_create_project(self):
		data = {
			"name": "New Project",
			"type": "Build",
			"status": "Planned",
			"priority": "Medium",
			"design_phase": "Phase 2",
			"customer": str(self.customer.id),
			"vessel": str(self.vessel.id),
			"start_date": "2025-02-01",
			"end_date": "2025-12-31",
			"manager": str(self.employee.id)
		}
		response = self.client.post("/projects/", data, format="json")
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

	def test_update_project(self):
		data = {
			"name": "Updated Project",
			"type": "Design",
			"status": "Completed",
			"priority": "Low",
			"design_phase": "Phase 3",
			"customer": str(self.customer.id),
			"vessel": str(self.vessel.id),
			"start_date": "2025-01-01",
			"end_date": "2025-12-31",
			"manager": str(self.employee.id)
		}
		response = self.client.put(f"/projects/{self.project.id}/", data, format="json")
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data["name"], "Updated Project")

	def test_delete_project(self):
		response = self.client.delete(f"/projects/{self.project.id}/")
		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
		self.assertFalse(Project.objects.filter(id=self.project.id).exists())
