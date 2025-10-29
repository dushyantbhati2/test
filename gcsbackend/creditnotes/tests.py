# creditnote/tests.py
import uuid
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from user.models import CustomUser
from customer.models import Customer
from .models import CreditNote
from rest_framework_simplejwt.tokens import RefreshToken


class CreditNoteAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create test user
        self.user = CustomUser.objects.create_user(
            username="testuser",
            password="testpass",
            type="hr"
        )

        # Generate JWT tokens
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

        self.customer = Customer.objects.create(
            id=uuid.uuid4(),
            customer_type="corporate",
            company_name="Test Customer Pvt Ltd",
            gst_number="22AAAAA0000A1Z5",
            pan_number="ABCDE1234F",
            gst_state="Maharashtra",
            gst_type="Regular",
            credit_terms_days=30,
            credit_limit=500000.00
        )

        self.credit_note = CreditNote.objects.create(
            note_number=1001,
            date="2025-01-01",
            customer=self.customer,
            reference="INV-123",
            reason="Overpayment",
            notes="Test note"
        )

    def test_list_creditnotes(self):
        response = self.client.get("/creditnotes/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_retrieve_creditnote(self):
        response = self.client.get(f"/creditnotes/{self.credit_note.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], str(self.credit_note.id))

    def test_create_creditnote(self):
        data = {
            "note_number": 1002,
            "date": "2025-02-01",
            "customer": str(self.customer.id),
            "reference": "INV-456",
            "reason": "Returned items",
            "notes": "Customer returned items"
        }
        response = self.client.post("/creditnotes/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["reason"], "Returned items")

    def test_update_creditnote(self):
        data = {
            "note_number": 1001,
            "date": "2025-01-01",
            "customer": str(self.customer.id),
            "reference": "INV-123-UPDATED",
            "reason": "Updated reason",
            "notes": "Updated notes"
        }
        response = self.client.put(f"/creditnotes/{self.credit_note.id}/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["reference"], "INV-123-UPDATED")

    def test_delete_creditnote(self):
        response = self.client.delete(f"/creditnotes/{self.credit_note.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(CreditNote.objects.filter(id=self.credit_note.id).exists())
