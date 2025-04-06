from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status
from rest_framework.test import force_authenticate

from itineraries.views.itinerary_activity_views import ItineraryActivityRetrieveAPIView, ItineraryActivityCreateAPIView, \
    ItineraryActivityUpdateAPIView, ItineraryActivityDestroyAPIView, ItineraryActivityListAPIView
from itineraries.views.itinerary_views import ItineraryCreateAPIView, ItineraryRetrieveAPIView, ItineraryUpdateAPIView, \
    ItineraryDestroyAPIView, ItineraryListAPIView
from users.models import CustomUser, UserProfile
from trips.models import Trip  # Assuming the Trip model is in the 'trips' app
from itineraries.models import Itinerary, ItineraryActivity


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
        response = view(request, trip_pk=self.trip.id)
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
        request = self.factory.get('/itineraries/all')
        force_authenticate(request, user=self.user)
        response = view(request, pk=self.itinerary.id, trip_pk=self.trip.id)
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


class ItineraryActivityAPITestCase(TestCase):
    def setUp(self):
        """
        Set up the test data, including a user, their profile, a trip, an itinerary, and an itinerary activity.
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
            settings={"currency": "USD"},
            start_date="2025-06-01",
            end_date="2025-06-15"
        )
        self.trip.members.add(self.user_profile)

        self.itinerary = Itinerary.objects.create(
            name="Trip to France",
            country="France",
            start_date="2025-06-05",
            end_date="2025-06-10",
            trip=self.trip
        )

        self.activity = ItineraryActivity.objects.create(
            name="Visit Eiffel Tower",
            type="Sightseeing",
            description="A guided tour to the Eiffel Tower.",
            location="Paris",
            start_time="10:00:00",
            duration=120,
            itinerary=self.itinerary
        )

    def test_activity_create(self):
        """
        Test creating an itinerary activity when the request is valid.
        """
        data = {
            'name': 'Louvre Museum Visit',
            'type': 'test1',
            'description': 'Visit to the Louvre Museum.',
            'location': 'Paris',
            'start_time': '12:00:00',
            'duration': 90,
            'itinerary': self.itinerary.id
        }
        view = ItineraryActivityCreateAPIView.as_view()
        url = f'/itineraries/{self.itinerary.id}/activities/create/'
        request = self.factory.post(url, data)
        force_authenticate(request, user=self.user)
        response = view(request, itinerary_pk=self.itinerary.id)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_activity_retrieve(self):
        """
        Test retrieving an itinerary activity.
        """
        view = ItineraryActivityRetrieveAPIView.as_view()
        request = self.factory.get(f'/activities/{self.activity.id}/')
        force_authenticate(request, user=self.user)
        response = view(request, pk=self.activity.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.activity.name)

    def test_activity_update(self):
        """
        Test updating an itinerary activity when the user is authenticated.
        """
        data = {
            'name': 'Updated Eiffel Tower Visit',
            'type': 'test1',
            'description': 'An updated guided tour.',
            'location': 'Paris',
            'start_time': '11:00:00',
            'duration': 150,
            'itinerary': self.itinerary.id
        }
        view = ItineraryActivityUpdateAPIView.as_view()
        request = self.factory.patch(f'/activities/{self.activity.id}/', data)
        force_authenticate(request, user=self.user)
        response = view(request, pk=self.activity.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.activity.refresh_from_db()
        self.assertEqual(self.activity.name, data['name'])

    def test_activity_destroy(self):
        """
        Test deleting an itinerary activity.
        """
        view = ItineraryActivityDestroyAPIView.as_view()
        request = self.factory.delete(f'/activities/{self.activity.id}/')
        force_authenticate(request, user=self.user)
        response = view(
            request,
            trip_pk=self.activity.itinerary.trip.pk,
            itinerary_pk=self.activity.itinerary.pk,
            pk=self.activity.id
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(ItineraryActivity.objects.filter(id=self.activity.id).exists())

    def test_activity_list(self):
        """
        Test listing all itinerary activities when the user is authenticated.
        """
        view = ItineraryActivityListAPIView.as_view()
        request = self.factory.get(f'/itineraries/{self.itinerary.id}/activities/all/')
        force_authenticate(request, user=self.user)
        response = view(request, itinerary_pk=self.itinerary.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

    def test_activity_create_unauthenticated(self):
        """
        Test creating an itinerary activity without authentication.
        """
        data = {
            'name': 'Notre Dame Visit',
            'type': 'Sightseeing',
            'description': 'Visit to the Notre Dame Cathedral.',
            'location': 'Paris',
            'start_time': '14:00:00',
            'duration': 60,
            'itinerary': self.itinerary.id
        }
        view = ItineraryActivityCreateAPIView.as_view()
        request = self.factory.post('/activities/', data)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_activity_update_unauthenticated(self):
        """
        Test updating an itinerary activity without authentication.
        """
        data = {
            'name': 'Unauthorized Update',
            'type': 'Tour',
            'description': 'Attempt to update without authentication.',
            'location': 'Paris',
            'start_time': '10:00:00',
            'duration': 90,
            'itinerary': self.itinerary.id
        }
        view = ItineraryActivityUpdateAPIView.as_view()
        request = self.factory.patch(f'/activities/{self.activity.id}/', data)
        response = view(request, pk=self.activity.id)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_activity_destroy_unauthenticated(self):
        """
        Test deleting an itinerary activity without authentication.
        """
        view = ItineraryActivityDestroyAPIView.as_view()
        request = self.factory.delete(f'/activities/{self.activity.id}/')
        response = view(request, pk=self.activity.id)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_activity_list_unauthenticated(self):
        """
        Test listing itinerary activities without authentication.
        """
        view = ItineraryActivityListAPIView.as_view()
        request = self.factory.get('/activities/')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
