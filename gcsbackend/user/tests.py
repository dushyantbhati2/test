
# user/tests.py
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken

class UserAPITest(TestCase):
	def setUp(self):
		self.client = APIClient()
		self.user = CustomUser.objects.create_user(
			username="testuser",
			password="testpass",
			type="hr"
		)
		refresh = RefreshToken.for_user(self.user)
		self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

	def test_list_users(self):
		response = self.client.get("/user/")
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_retrieve_user(self):
		response = self.client.get(f"/user/{self.user.id}/")
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_create_user(self):
		data = {
			"username": "newuser",
			"password": "newpass",
			"type": "employee"
		}
		response = self.client.post("/user/", data, format="json")
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

	def test_update_user(self):
		data = {
			"username": "updateduser",
			"type": "hr"
		}
		response = self.client.put(f"/user/{self.user.id}/", data, format="json")
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data["username"], "updateduser")

	def test_delete_user(self):
		response = self.client.delete(f"/user/{self.user.id}/")
		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
		self.assertFalse(CustomUser.objects.filter(id=self.user.id).exists())
