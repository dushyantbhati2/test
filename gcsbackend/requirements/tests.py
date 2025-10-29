# requirement/tests.py
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from user.models import CustomUser
from projects.models import Project
from employee.models import Employee, Department
from customer.models import Customer
from vessels.models import Vessel
from .models import Requirement

class RequirementAPITest(TestCase):
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
            manager=self.employee,
            budget=10000,
            value=50000
        )

        # Create a Requirement instance
        self.requirement = Requirement.objects.create(
            title="Requirement 1",
            project=self.project,
            description="Requirement description",
            type="Functional",
            priority="High",
            status="Open"
        )

    def test_list_requirements(self):
        response = self.client.get("/requirements/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_retrieve_requirement(self):
        response = self.client.get(f"/requirements/{self.requirement.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Requirement 1")

    def test_create_requirement(self):
        data = {
            "title": "Requirement 2",
            "project": str(self.project.id),
            "description": "New requirement description",
            "type": "Non-Functional",
            "priority": "Medium",
            "status": "Open"
        }
        response = self.client.post("/requirements/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "Requirement 2")

    def test_update_requirement(self):
        data = {
            "title": "Requirement 1 Updated",
            "status": "Closed"
        }
        response = self.client.patch(f"/requirements/{self.requirement.id}/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Requirement 1 Updated")
        self.assertEqual(response.data["status"], "Closed")

    def test_delete_requirement(self):
        response = self.client.delete(f"/requirements/{self.requirement.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Requirement.objects.filter(id=self.requirement.id).exists())
