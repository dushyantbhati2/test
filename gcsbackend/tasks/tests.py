
# tasks/tests.py
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from user.models import CustomUser
from employee.models import Employee
from projects.models import Project
from customer.models import Customer
from vessels.models import Vessel
from .models import Task
from rest_framework_simplejwt.tokens import RefreshToken
from employee.models import Department
class TaskAPITest(TestCase):
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
			manager=Employee.objects.create(
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
		)
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
		self.task = Task.objects.create(
			project=self.project,
			title="Test Task",
			assigned_to=self.employee,
			due_date="2025-06-01",
			status="Open",
			priority="High",
			estimated_hours=10,
			completion=0
		)

	def test_list_tasks(self):
		response = self.client.get("/tasks/")
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_retrieve_task(self):
		response = self.client.get(f"/tasks/{self.task.id}/")
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_create_task(self):
		data = {
			"project": str(self.project.id),
			"title": "New Task",
			"assigned_to": str(self.employee.id),
			"due_date": "2025-07-01",
			"status": "Pending",
			"priority": "Medium",
			"estimated_hours": 5,
			"completion": 0,
			"plan_number": "PN-001",           
    		"revision": "A" 
		}
		response = self.client.post("/tasks/", data, format="json")
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

	def test_update_task(self):
		data = {
			"project": str(self.project.id),
			"title": "Updated Task",
			"assigned_to": str(self.employee.id),
			"due_date": "2025-06-01",
			"status": "Completed",
			"priority": "Low",
			"estimated_hours": 8,
			"completion": 100
		}
		response = self.client.patch(f"/tasks/{self.task.id}/", data, format="json")
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data["title"], "Updated Task")

	def test_delete_task(self):
		response = self.client.delete(f"/tasks/{self.task.id}/")
		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
		self.assertFalse(Task.objects.filter(id=self.task.id).exists())
