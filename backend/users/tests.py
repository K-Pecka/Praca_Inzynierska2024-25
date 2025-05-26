from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status
from rest_framework.test import force_authenticate

from users.models import CustomUser, UserProfileType
from users.views.user_views import UserCreateAPIView, UserUpdatePasswordAPIView, UserUpdateAPIView


class UserAPITestCase(TestCase):
    def setUp(self):
        """
        Setup a test user, generate a token for them, and set up URLs.
        """
        self.factory = APIRequestFactory()
        self.user_profile_type = UserProfileType.objects.create(
            code="tourist",
            name="Turysta",
        )
        self.user = CustomUser.objects.create_user(
            email="jacob@…",
            password="Top_secret12",
            first_name="jacob",
            last_name="ereres",
            )

    def test_user_create(self):
        """
        Test creating a user when the request is valid.
        """
        data = {
            'email': 'newuser@example.com',
            'password': 'NewPassword123',
            'first_name': 'New',
            'last_name': 'User',
        }
        view = UserCreateAPIView.as_view()
        request = self.factory.post('/user/', data)
        response = view(request)
        print(response.__dict__)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_update_password(self):
        """
        Test updating the user's password when the user is authenticated.
        """
        data = {
            'password': 'NewPassword456',
        }
        user = CustomUser.objects.filter(pk=1).first()
        view = UserUpdatePasswordAPIView.as_view()
        request = self.factory.patch('/user/password/', data)
        force_authenticate(request, user=user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_update_password_unauthenticated(self):
        """
        Test updating the user's password when the user is authenticated.
        """
        data = {
            'password': 'NewPassword456',
        }
        view = UserUpdatePasswordAPIView.as_view()
        request = self.factory.patch('/user/password/', data)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_update(self):
        """
        Test that trying to update the user profile without authentication returns 401.
        """
        data = {
            'email': 'newuser@example.com',
            'password': 'NewPassword123',
            'password_confirm': 'NewPassword123',
            'first_name': 'New',
            'last_name': 'User',
        }
        user = CustomUser.objects.filter(pk=1).first()
        view = UserUpdateAPIView.as_view()
        request = self.factory.patch('/user/', data)
        force_authenticate(request, user=user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_update_unauthenticated(self):
        """
        Test that trying to update the user profile without authentication returns 401.
        """
        data = {
            'email': 'newuser@example.com',
            'password': 'NewPassword123',
            'first_name': 'New',
            'last_name': 'User',
        }
        view = UserUpdateAPIView.as_view()
        request = self.factory.post('/user/', data)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
