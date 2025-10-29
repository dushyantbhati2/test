
# vessels/tests.py
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from user.models import CustomUser
from customer.models import Customer
from .models import Vessel
from rest_framework_simplejwt.tokens import RefreshToken

class VesselAPITest(TestCase):
	def setUp(self):
		self.client = APIClient()
		self.user = CustomUser.objects.create_user(
			username="testuser",
			password="testpass",
			type="hr"
		)
		refresh = RefreshToken.for_user(self.user)
		self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
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

	def test_list_vessels(self):
		response = self.client.get("/vessels/")
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_retrieve_vessel(self):
		response = self.client.get(f"/vessels/{self.vessel.id}/")
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_create_vessel(self):
		data = {
			"name": "New Vessel",
			"imo_number": "IMO7654321",
			"type": "Tanker",
			"owner": str(self.customer.id)
		}
		response = self.client.post("/vessels/", data, format="json")
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

	def test_update_vessel(self):
		data = {
			"name": "Updated Vessel",
			"imo_number": "IMO1234567",
			"type": "Cargo",
			"owner": str(self.customer.id)
		}
		response = self.client.put(f"/vessels/{self.vessel.id}/", data, format="json")
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data["name"], "Updated Vessel")

	def test_delete_vessel(self):
		response = self.client.delete(f"/vessels/{self.vessel.id}/")
		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
		self.assertFalse(Vessel.objects.filter(id=self.vessel.id).exists())
