from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status
from rest_framework.test import force_authenticate

from users.models import CustomUser, UserProfile
from trips.models import Trip  # Assuming the Trip model is in the 'trips' app
from itineraries.api_views import ItineraryCreateAPIView, ItineraryRetrieveAPIView, ItineraryUpdateAPIView, \
    ItineraryDestroyAPIView, ItineraryListAPIView
from itineraries.models import Itinerary


class ItineraryAPITestCase(TestCase):
    def setUp(self):
        """
        Set up the test data, including a user, their profile, a trip, and an itinerary.
        """
        self.factory = APIRequestFactory()

        self.user = CustomUser.objects.create_user(
            email="testuser@example.com",
            password="TestPassword123",
            date_of_birth="19000101",
            first_name="Test",
            last_name="User",
        )
        self.user_profile, created = UserProfile.objects.get_or_create(user=self.user)

        self.trip = Trip.objects.create(
            creator=self.user_profile,
            budget=1000.00,
            settings={"currency": "USD"},
            start_date="2025-06-01",
            end_date="2025-06-10"
        )

        self.trip.members.add(self.user_profile)

        self.itinerary = Itinerary.objects.create(
            name="Eiffel Tower Visit",
            country="France",
            start_date="2025-06-02",
            end_date="2025-06-02",
            trip=self.trip
        )

    def test_itinerary_create(self):
        """
        Test creating an itinerary when the request is valid.
        """
        data = {
            'name': 'Trip to New York Itinerary',
            'country': 'USA',
            'start_date': '2025-07-01',
            'end_date': '2025-07-10',
            'trip': self.trip.id
        }
        view = ItineraryCreateAPIView.as_view()
        request = self.factory.post('/itineraries/', data)
        force_authenticate(request, user=self.user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_itinerary_retrieve(self):
        """
        Test retrieving an itinerary.
        """
        view = ItineraryRetrieveAPIView.as_view()
        request = self.factory.get(f'/itineraries/{self.itinerary.id}/')
        force_authenticate(request, user=self.user)
        response = view(request, pk=self.itinerary.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.itinerary.name)

    def test_itinerary_update(self):
        """
        Test updating an itinerary when the user is authenticated.
        """
        data = {
            'name': 'Updated Trip to Paris Itinerary',
            'country': 'France',
            'start_date': '2025-06-05',
            'end_date': '2025-06-20',
            'trip': self.trip.id
        }
        view = ItineraryUpdateAPIView.as_view()
        request = self.factory.patch(f'/itineraries/{self.itinerary.id}/', data)
        force_authenticate(request, user=self.user)
        response = view(request, pk=self.itinerary.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.itinerary.refresh_from_db()
        self.assertEqual(self.itinerary.name, data['name'])

    def test_itinerary_destroy(self):
        """
        Test deleting an itinerary.
        """
        view = ItineraryDestroyAPIView.as_view()
        request = self.factory.delete(f'/itineraries/{self.itinerary.id}/')
        force_authenticate(request, user=self.user)
        response = view(request, pk=self.itinerary.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Itinerary.objects.filter(id=self.itinerary.id).exists())

    def test_itinerary_list(self):
        """
        Test listing all itineraries when the user is authenticated.
        """
        view = ItineraryListAPIView.as_view()
        request = self.factory.get('/itineraries/')
        force_authenticate(request, user=self.user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_itinerary_create_unauthenticated(self):
        """
        Test creating an itinerary without authentication.
        """
        data = {
            'name': 'Trip to Rome Itinerary',
            'country': 'Italy',
            'start_date': '2025-08-01',
            'end_date': '2025-08-10',
            'trip': self.trip.id
        }
        view = ItineraryCreateAPIView.as_view()
        request = self.factory.post('/itineraries/', data)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_itinerary_update_unauthenticated(self):
        """
        Test updating an itinerary without authentication.
        """
        data = {
            'name': 'Updated Trip to Rome Itinerary',
            'country': 'Italy',
            'start_date': '2025-08-05',
            'end_date': '2025-08-15',
            'trip': self.trip.id
        }
        view = ItineraryUpdateAPIView.as_view()
        request = self.factory.patch(f'/itineraries/{self.itinerary.id}/', data)
        response = view(request, pk=self.itinerary.id)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_itinerary_destroy_unauthenticated(self):
        """
        Test deleting an itinerary without authentication.
        """
        view = ItineraryDestroyAPIView.as_view()
        request = self.factory.delete(f'/itineraries/{self.itinerary.id}/')
        response = view(request, pk=self.itinerary.id)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_itinerary_list_unauthenticated(self):
        """
        Test listing itineraries without authentication.
        """
        view = ItineraryListAPIView.as_view()
        request = self.factory.get('/itineraries/')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
