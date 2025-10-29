# customer/tests.py
import uuid
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from user.models import CustomUser
from .models import Customer
from rest_framework_simplejwt.tokens import RefreshToken


class CustomerAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create test user with JWT
        self.user = CustomUser.objects.create_user(
            username="testuser",
            password="testpass",
            type="hr"
        )
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

        # Create base customer
        self.customer = Customer.objects.create(
            id=uuid.uuid4(),
            customer_type="Company",
            company_name="Test Company",
            gst_number="22AAAAA0000A1Z5",
            pan_number="ABCDE1234F",
            gst_state="Karnataka",
            gst_type="Regular",
            credit_terms_days=30,
            credit_limit=10000.00,
        )

    def test_list_customers(self):
        response = self.client.get("/customer/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_retrieve_customer(self):
        response = self.client.get(f"/customer/{self.customer.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], str(self.customer.id))

    def test_create_customer_with_contacts_and_addresses(self):
        data = {
            "customer_type": "Individual",
            "company_name": "New Customer",
            "gst_number": "22BBBBB0000B1Z5",
            "pan_number": "FGHIJ5678K",
            "gst_state": "Maharashtra",
            "gst_type": "Composition",
            "credit_terms_days": 15,
            "credit_limit": "5000.00",
            "contacts": [
                {
                    "title": "Mr",
                    "first_name": "John",
                    "last_name": "Doe",
                    "email": "john@example.com",
                    "phone": "9876543210",
                    "is_primary": True
                }
            ],
            "addresses": [
                {
                    "address_type": "Billing",
                    "address_line1": "123 Street",
                    "city": "Mumbai",
                    "state": "MH",
                    "postal_code": "400001",
                    "country": "India"
                }
            ]
        }
        response = self.client.post("/customer/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["company_name"], "New Customer")
        self.assertEqual(len(response.data["contacts"]), 1)
        self.assertEqual(len(response.data["addresses"]), 1)

    def test_update_customer(self):
        data = {
            "customer_type": "Company",
            "company_name": "Updated Company",
            "gst_number": "22AAAAA0000A1Z5",
            "pan_number": "ABCDE1234F",
            "gst_state": "Karnataka",
            "gst_type": "Regular",
            "credit_terms_days": 45,
            "credit_limit": "15000.00",
            "contacts": [],
            "addresses": []
        }

        response = self.client.patch(f"/customer/{self.customer.id}/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["company_name"], "Updated Company")
        self.assertEqual(int(response.data["credit_terms_days"]), 45)

    def test_delete_customer(self):
        response = self.client.delete(f"/customer/{self.customer.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # custom response
        self.assertFalse(Customer.objects.filter(id=self.customer.id).exists())
