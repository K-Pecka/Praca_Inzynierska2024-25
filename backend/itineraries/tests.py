from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status
from rest_framework.test import force_authenticate

from itineraries.views.itinerary_activity_views import ItineraryActivityViewSet
from itineraries.views.itinerary_views import ItineraryViewSet
from users.models import CustomUser, UserProfile, UserProfileType
from trips.models import Trip
from itineraries.models import Itinerary, ItineraryActivity, ItineraryActivityType


class ItineraryAPITestCase(TestCase):
    def setUp(self):
        """
        Set up the test data, including a user, their profile, a trip, and an itinerary.
        """
        self.factory = APIRequestFactory()
        self.default_user_profile = UserProfileType.objects.create(
            code="tourist",
            name="Tourist",
        )
        self.user = CustomUser.objects.create_user(
            email="testuser@example.com",
            password="TestPassword123",
            first_name="Test",
            last_name="User",
            subscription_plan="guide",
            subscription_active=True,
        )
        self.user_profile, created = UserProfile.objects.get_or_create(user=self.user)

        self.member_user = CustomUser.objects.create_user(
            email="membertestuser@example.com",
            password="TestPassword123",
            first_name="Member",
            last_name="User",
            subscription_plan="tourist",
            subscription_active=True,
        )
        self.member_user_profile, created = UserProfile.objects.get_or_create(user=self.member_user)

        self.not_member_user = CustomUser.objects.create_user(
            email="testnonmemberuser@example.com",
            password="TestPassword123",
            first_name="Test",
            last_name="NonMember",
            subscription_plan="tourist",
            subscription_active=True,
        )
        self.not_member_user_profile, created = UserProfile.objects.get_or_create(user=self.not_member_user)

        self.trip = Trip.objects.create(
            creator=self.user_profile,
            settings={"currency": "USD"},
            start_date="2025-06-01",
            end_date="2025-06-10"
        )

        self.trip.members.add(self.member_user_profile)

        self.itinerary = Itinerary.objects.create(
            name="Eiffel Tower Visit",
            country="France",
            start_date="2025-06-02",
            end_date="2025-06-02",
            trip=self.trip
        )

    ########################################################################
    # TEST CASES FOR ITINERARY ENDPOINTS - CREATE
    ########################################################################
    def test_itinerary_create_as_guide_owner(self):
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
        view = ItineraryViewSet.as_view({'post': 'create'})
        request = self.factory.post('/itineraries/', data)
        force_authenticate(request, user=self.user)
        response = view(request, trip_pk=self.trip.id)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_itinerary_create_as_free_account_owner(self):
        """
        Test creating an itinerary when the user is a free account owner.
        """
        self.user.subscription_plan = 'free'
        self.user.save()

        data = {
            'name': 'Trip to London Itinerary',
            'country': 'UK',
            'start_date': '2025-08-01',
            'end_date': '2025-08-10',
            'trip': self.trip.id
        }
        view = ItineraryViewSet.as_view({'post': 'create'})
        request = self.factory.post('/itineraries/', data)
        force_authenticate(request, user=self.user)
        response = view(request, trip_pk=self.trip.id)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_itinerary_create_as_tourist_account_owner(self):
        """
        Test creating an itinerary when the user is a tourist.
        """
        self.user.subscription_plan = 'tourist'
        self.user.save()

        data = {
            'name': 'Trip to Tokyo Itinerary',
            'country': 'Japan',
            'start_date': '2025-09-01',
            'end_date': '2025-09-10',
            'trip': self.trip.id
        }
        view = ItineraryViewSet.as_view({'post': 'create'})
        request = self.factory.post('/itineraries/', data)
        force_authenticate(request, user=self.user)
        response = view(request, trip_pk=self.trip.id)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_itinerary_create_as_member_user(self):
        """
        Test creating an itinerary when the user is a member of the trip.
        """
        data = {
            'name': 'Trip to Paris Itinerary',
            'country': 'France',
            'start_date': '2025-06-01',
            'end_date': '2025-06-10',
            'trip': self.trip.id
        }
        view = ItineraryViewSet.as_view({'post': 'create'})
        request = self.factory.post('/itineraries/', data)
        force_authenticate(request, user=self.member_user)
        response = view(request, trip_pk=self.trip.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_itinerary_create_as_not_member_user(self):
        """
        Test creating an itinerary when the user is not a member of the trip.
        """
        data = {
            'name': 'Unauthorized Trip to Rome Itinerary',
            'country': 'Italy',
            'start_date': '2025-08-01',
            'end_date': '2025-08-10',
            'trip': self.trip.id
        }
        view = ItineraryViewSet.as_view({'post': 'create'})
        request = self.factory.post('/itineraries/', data)
        force_authenticate(request, user=self.not_member_user)
        response = view(request, trip_pk=self.trip.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

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
        view = ItineraryViewSet.as_view({'post': 'create'})
        request = self.factory.post('/itineraries/', data)
        response = view(request, trip_pk=self.trip.id)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    ########################################################################
    # TEST CASES FOR ITINERARY ENDPOINTS - RETRIEVE
    ########################################################################

    def test_itinerary_retrieve(self):
        """
        Test retrieving an itinerary.
        """
        view = ItineraryViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get(f'/itineraries/{self.itinerary.id}/')
        force_authenticate(request, user=self.user)
        response = view(request, trip_pk=self.trip.id, pk=self.itinerary.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.itinerary.name)

    def test_itinerary_retrieve_as_not_member(self):
        """
        Test retrieving an itinerary when the user is not a member of the trip.
        """
        view = ItineraryViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get(f'/itineraries/{self.itinerary.id}/')
        force_authenticate(request, user=self.not_member_user)
        response = view(request, trip_pk=self.trip.id, pk=self.itinerary.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    ########################################################################
    # TEST CASES FOR ITINERARY ENDPOINTS - UPDATE
    ########################################################################

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
        view = ItineraryViewSet.as_view({'patch': 'partial_update'})
        request = self.factory.patch(f'/itineraries/{self.itinerary.id}/', data)
        force_authenticate(request, user=self.user)
        response = view(request, trip_pk=self.trip.id, pk=self.itinerary.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.itinerary.refresh_from_db()
        self.assertEqual(self.itinerary.name, data['name'])

    def test_itinerary_update_as_member_user(self):
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
        view = ItineraryViewSet.as_view({'patch': 'partial_update'})
        request = self.factory.patch(f'/itineraries/{self.itinerary.id}/', data)
        force_authenticate(request, user=self.member_user)
        response = view(request, trip_pk=self.trip.id, pk=self.itinerary.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.itinerary.refresh_from_db()
        self.assertEqual(self.itinerary.name, 'Eiffel Tower Visit')

    def test_itinerary_update_as_not_member_user(self):
        """
        Test updating an itinerary when the user is not a member of the trip.
        """
        data = {
            'name': 'Unauthorized Update',
            'country': 'France',
            'start_date': '2025-06-05',
            'end_date': '2025-06-20',
            'trip': self.trip.id
        }
        view = ItineraryViewSet.as_view({'patch': 'partial_update'})
        request = self.factory.patch(f'/itineraries/{self.itinerary.id}/', data)
        force_authenticate(request, user=self.not_member_user)
        response = view(request, trip_pk=self.trip.id, pk=self.itinerary.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.itinerary.refresh_from_db()
        self.assertEqual(self.itinerary.name, 'Eiffel Tower Visit')

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
        view = ItineraryViewSet.as_view({'patch': 'partial_update'})
        request = self.factory.patch(f'/itineraries/{self.itinerary.id}/', data)
        response = view(request, trip_pk=self.trip.id, pk=self.itinerary.id)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    ########################################################################
    # TEST CASES FOR ITINERARY ENDPOINTS - DESTROY
    ########################################################################

    def test_itinerary_destroy(self):
        """
        Test deleting an itinerary.
        """
        view = ItineraryViewSet.as_view({'delete': 'destroy'})
        request = self.factory.delete(f'/itineraries/{self.itinerary.id}/')
        force_authenticate(request, user=self.user)
        response = view(request, trip_pk=self.trip.id, pk=self.itinerary.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Itinerary.objects.filter(id=self.itinerary.id).exists())

    def test_itinerary_destroy_as_not_member_user(self):
        """
        Test deleting an itinerary.
        """
        view = ItineraryViewSet.as_view({'delete': 'destroy'})
        request = self.factory.delete(f'/itineraries/{self.itinerary.id}/')
        force_authenticate(request, user=self.not_member_user)
        response = view(request, trip_pk=self.trip.id, pk=self.itinerary.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Itinerary.objects.filter(id=self.itinerary.id).exists())

    def test_itinerary_destroy_as_member_user(self):
        """
        Test deleting an itinerary.
        """
        view = ItineraryViewSet.as_view({'delete': 'destroy'})
        request = self.factory.delete(f'/itineraries/{self.itinerary.id}/')
        force_authenticate(request, user=self.member_user)
        response = view(request, trip_pk=self.trip.id, pk=self.itinerary.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Itinerary.objects.filter(id=self.itinerary.id).exists())

    def test_itinerary_destroy_unauthenticated(self):
        """
        Test deleting an itinerary without authentication.
        """
        view = ItineraryViewSet.as_view({'delete': 'destroy'})
        request = self.factory.delete(f'/itineraries/{self.itinerary.id}/')
        response = view(request, trip_pk=self.trip.id, pk=self.itinerary.id)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    ########################################################################
    # TEST CASES FOR ITINERARY ENDPOINTS - LIST
    ########################################################################

    def test_itinerary_list(self):
        """
        Test listing all itineraries when the user is authenticated.
        """
        view = ItineraryViewSet.as_view({'get': 'list'})
        request = self.factory.get('/itineraries/all')
        force_authenticate(request, user=self.user)
        response = view(request, trip_pk=self.trip.id, pk=self.itinerary.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_itinerary_list_as_not_member_user(self):
        """
        Test listing all itineraries when the user is authenticated.
        """
        view = ItineraryViewSet.as_view({'get': 'list'})
        request = self.factory.get('/itineraries/all')
        force_authenticate(request, user=self.not_member_user)
        response = view(request, trip_pk=self.trip.id, pk=self.itinerary.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_itinerary_list_unauthenticated(self):
        """
        Test listing itineraries without authentication.
        """
        view = ItineraryViewSet.as_view({'get': 'list'})
        request = self.factory.get('/itineraries/')
        response = view(request, trip_pk=self.trip.id)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ItineraryActivityAPITestCase(TestCase):
    def setUp(self):
        """
        Set up the test data, including a user, their profile, a trip, an itinerary, and an itinerary activity.
        """
        self.factory = APIRequestFactory()
        self.default_user_profile = UserProfileType.objects.create(
            code="tourist",
            name="Tourist",
        )
        self.user = CustomUser.objects.create_user(
            email="testuser@example.com",
            password="TestPassword123",
            first_name="Test",
            last_name="User",
            subscription_plan="guide",
            subscription_active=True,
        )
        self.user_profile, created = UserProfile.objects.get_or_create(user=self.user)

        self.member_user = CustomUser.objects.create_user(
            email="membertestuser@example.com",
            password="TestPassword123",
            first_name="Member",
            last_name="User",
            subscription_plan="tourist",
            subscription_active=True,
        )
        self.member_user_profile, created = UserProfile.objects.get_or_create(user=self.member_user)

        self.not_member_user = CustomUser.objects.create_user(
            email="testnonmemberuser@example.com",
            password="TestPassword123",
            first_name="Test",
            last_name="NonMember",
            subscription_plan="tourist",
            subscription_active=True,
        )
        self.not_member_user_profile, created = UserProfile.objects.get_or_create(user=self.not_member_user)


        self.trip = Trip.objects.create(
            creator=self.user_profile,
            settings={"currency": "USD"},
            start_date="2025-06-01",
            end_date="2025-06-15"
        )
        self.trip.members.add(self.member_user_profile)

        self.itinerary = Itinerary.objects.create(
            name="Trip to France",
            country="France",
            start_date="2025-06-05",
            end_date="2025-06-10",
            trip=self.trip
        )

        self.itinerary_activity_type = ItineraryActivityType.objects.create(
            name="Sightseeing",
        )

        self.activity = ItineraryActivity.objects.create(
            name="Visit Eiffel Tower",
            type=self.itinerary_activity_type,
            description="A guided tour to the Eiffel Tower.",
            location="Paris",
            date="2025-06-06",
            start_time="10:00:00",
            duration=120,
            itinerary=self.itinerary
        )

    ########################################################################
    # TEST CASES FOR ITINERARY ACTIVITY ENDPOINTS - CREATE
    ########################################################################

    def test_activity_create_as_guide_account_owner(self):
        """
        Test creating an itinerary activity when the request is valid.
        """
        data = {
            'name': 'Louvre Museum Visit',
            'type': self.itinerary_activity_type.id,
            'description': 'Visit to the Louvre Museum.',
            'location': 'Paris',
            'date': '2025-06-07',
            'start_time': '12:00:00',
            'duration': 90,
            'itinerary': self.itinerary.id
        }
        view = ItineraryActivityViewSet.as_view({'post': 'create'})
        url = f'/itineraries/{self.itinerary.id}/activities/create/'
        request = self.factory.post(url, data)
        force_authenticate(request, user=self.user)
        response = view(request, itinerary_pk=self.itinerary.id)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_activity_create_as_tourist_account_owner(self):
        """
        Test creating an itinerary activity when the user is a tourist.
        """
        self.user.subscription_plan = 'tourist'
        self.user.save()

        data = {
            'name': 'Notre Dame Visit',
            'type': self.itinerary_activity_type.id,
            'description': 'Visit to the Notre Dame Cathedral.',
            'location': 'Paris',
            'date': '2025-06-08',
            'start_time': '14:00:00',
            'duration': 60,
            'itinerary': self.itinerary.id
        }
        view = ItineraryActivityViewSet.as_view({'post': 'create'})
        request = self.factory.post(f'/itineraries/{self.itinerary.id}/activities/create/', data)
        force_authenticate(request, user=self.user)
        response = view(request, itinerary_pk=self.itinerary.id)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_activity_create_as_free_account_owner(self):
        """
        Test creating an itinerary activity when the user is a free account owner.
        """
        self.user.subscription_plan = 'free'
        self.user.save()

        data = {
            'name': 'Unauthorized Activity',
            'type': self.itinerary_activity_type.id,
            'description': 'This should not be allowed.',
            'location': 'Paris',
            'date': '2025-06-09',
            'start_time': '15:00:00',
            'duration': 30,
            'itinerary': self.itinerary.id
        }
        view = ItineraryActivityViewSet.as_view({'post': 'create'})
        request = self.factory.post(f'/itineraries/{self.itinerary.id}/activities/create/', data)
        force_authenticate(request, user=self.user)
        response = view(request, itinerary_pk=self.itinerary.id)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_activity_create_as_member_user(self):
        """
        Test creating an itinerary activity when the user is a member of the trip.
        """
        data = {
            'name': 'Member Activity',
            'type': self.itinerary_activity_type.id,
            'description': 'This is a member activity.',
            'location': 'Paris',
            'date': '2025-06-10',
            'start_time': '16:00:00',
            'duration': 45,
            'itinerary': self.itinerary.id
        }
        view = ItineraryActivityViewSet.as_view({'post': 'create'})
        request = self.factory.post(f'/itineraries/{self.itinerary.id}/activities/create/', data)
        force_authenticate(request, user=self.member_user)
        response = view(request, itinerary_pk=self.itinerary.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_activity_create_as_not_member_user(self):
        """
        Test creating an itinerary activity when the user is not a member of the trip.
        """
        data = {
            'name': 'Unauthorized Activity',
            'type': self.itinerary_activity_type.id,
            'description': 'This should not be allowed.',
            'location': 'Paris',
            'date': '2025-06-11',
            'start_time': '17:00:00',
            'duration': 30,
            'itinerary': self.itinerary.id
        }
        view = ItineraryActivityViewSet.as_view({'post': 'create'})
        request = self.factory.post(f'/itineraries/{self.itinerary.id}/activities/create/', data)
        force_authenticate(request, user=self.not_member_user)
        response = view(request, itinerary_pk=self.itinerary.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_activity_create_unauthenticated(self):
        """
        Test creating an itinerary activity without authentication.
        """
        data = {
            'name': 'Notre Dame Visit',
            'type': self.itinerary_activity_type.id,
            'description': 'Visit to the Notre Dame Cathedral.',
            'location': 'Paris',
            'date': '2025-06-09',
            'start_time': '14:00:00',
            'duration': 60,
            'itinerary': self.itinerary.id
        }
        view = ItineraryActivityViewSet.as_view({'post': 'create'})
        request = self.factory.post('/activities/', data)
        response = view(request, itinerary_pk=self.itinerary.pk)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    ########################################################################
    # TEST CASES FOR ITINERARY ACTIVITY ENDPOINTS - RETRIEVE
    ########################################################################

    def test_activity_retrieve_as_creator(self):
        """
        Test retrieving an itinerary activity.
        """
        view = ItineraryActivityViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get(f'/activities/{self.activity.id}/')
        force_authenticate(request, user=self.user)
        response = view(request, itinerary_pk=self.itinerary.pk, pk=self.activity.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.activity.name)

    def test_activity_retrieve_as_member(self):
        """
        Test retrieving an itinerary activity as a member of the trip.
        """
        view = ItineraryActivityViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get(f'/activities/{self.activity.id}/')
        force_authenticate(request, user=self.member_user)
        response = view(request, itinerary_pk=self.itinerary.pk, pk=self.activity.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.activity.name)

    def test_activity_retrieve_as_not_member(self):
        """
        Test retrieving an itinerary activity as a user not a member of the trip.
        """
        view = ItineraryActivityViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get(f'/activities/{self.activity.id}/')
        force_authenticate(request, user=self.not_member_user)
        response = view(request, itinerary_pk=self.itinerary.pk, pk=self.activity.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    ########################################################################
    # TEST CASES FOR ITINERARY ACTIVITY ENDPOINTS - UPDATE
    ########################################################################

    def test_activity_update_as_creator(self):
        """
        Test updating an itinerary activity when the user is authenticated.
        """
        data = {
            'name': 'Updated Eiffel Tower Visit',
            'type': self.itinerary_activity_type.id,
            'description': 'An updated guided tour.',
            'location': 'Paris',
            'date': '2025-06-08',
            'start_time': '11:00:00',
            'duration': 150,
            'itinerary': self.itinerary.id
        }
        view = ItineraryActivityViewSet.as_view({'patch': 'partial_update'})
        request = self.factory.patch(f'/activities/{self.activity.id}/', data)
        force_authenticate(request, user=self.user)
        response = view(request, itinerary_pk=self.itinerary.pk, pk=self.activity.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.activity.refresh_from_db()
        self.assertEqual(self.activity.name, data['name'])

    def test_activity_update_as_member(self):
        """
        Test updating an itinerary activity when the user is a member of the trip.
        """
        data = {
            'name': 'Member Update',
            'type': self.itinerary_activity_type.id,
            'description': 'This is a member update.',
            'location': 'Paris',
            'date': '2025-06-09',
            'start_time': '12:00:00',
            'duration': 60,
            'itinerary': self.itinerary.id
        }
        view = ItineraryActivityViewSet.as_view({'patch': 'partial_update'})
        request = self.factory.patch(f'/activities/{self.activity.id}/', data)
        force_authenticate(request, user=self.member_user)
        response = view(request, itinerary_pk=self.itinerary.pk, pk=self.activity.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.activity.refresh_from_db()
        self.assertNotEqual(self.activity.name, data['name'])

    def test_activity_update_as_not_member(self):
        """
        Test updating an itinerary activity when the user is not a member of the trip.
        """
        data = {
            'name': 'Unauthorized Update',
            'type': self.itinerary_activity_type.id,
            'description': 'This should not be allowed.',
            'location': 'Paris',
            'date': '2025-06-10',
            'start_time': '13:00:00',
            'duration': 30,
            'itinerary': self.itinerary.id
        }
        view = ItineraryActivityViewSet.as_view({'patch': 'partial_update'})
        request = self.factory.patch(f'/activities/{self.activity.id}/', data)
        force_authenticate(request, user=self.not_member_user)
        response = view(request, itinerary_pk=self.itinerary.pk, pk=self.activity.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.activity.refresh_from_db()
        self.assertNotEqual(self.activity.name, data['name'])


    def test_activity_update_unauthenticated(self):
        """
        Test updating an itinerary activity without authentication.
        """
        data = {
            'name': 'Unauthorized Update',
            'type': self.itinerary_activity_type.id,
            'description': 'Attempt to update without authentication.',
            'location': 'Paris',
            'date': '2025-06-10',
            'start_time': '10:00:00',
            'duration': 90,
            'itinerary': self.itinerary.id
        }
        view = ItineraryActivityViewSet.as_view({'patch': 'partial_update'})
        request = self.factory.patch(f'/activities/{self.activity.id}/', data)
        response = view(request, pk=self.activity.id)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    ########################################################################
    # TEST CASES FOR ITINERARY ACTIVITY ENDPOINTS - DESTROY
    ########################################################################

    def test_activity_destroy(self):
        """
        Test deleting an itinerary activity.
        """
        view = ItineraryActivityViewSet.as_view({'delete': 'destroy'})
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

    def test_activity_destroy_as_member(self):
        """
        Test deleting an itinerary activity as a member of the trip.
        """
        view = ItineraryActivityViewSet.as_view({'delete': 'destroy'})
        request = self.factory.delete(f'/activities/{self.activity.id}/')
        force_authenticate(request, user=self.member_user)
        response = view(
            request,
            trip_pk=self.activity.itinerary.trip.pk,
            itinerary_pk=self.activity.itinerary.pk,
            pk=self.activity.id
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(ItineraryActivity.objects.filter(id=self.activity.id).exists())

    def test_activity_destroy_as_not_member(self):
        """
        Test deleting an itinerary activity as a user not a member of the trip.
        """
        view = ItineraryActivityViewSet.as_view({'delete': 'destroy'})
        request = self.factory.delete(f'/activities/{self.activity.id}/')
        force_authenticate(request, user=self.not_member_user)
        response = view(
            request,
            trip_pk=self.activity.itinerary.trip.pk,
            itinerary_pk=self.activity.itinerary.pk,
            pk=self.activity.id
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(ItineraryActivity.objects.filter(id=self.activity.id).exists())

    def test_activity_destroy_unauthenticated(self):
        """
        Test deleting an itinerary activity without authentication.
        """
        view = ItineraryActivityViewSet.as_view({'delete': 'destroy'})
        request = self.factory.delete(f'/activities/{self.activity.id}/')
        response = view(request, itinerary_pk=self.itinerary.pk, pk=self.activity.id)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    ########################################################################
    # TEST CASES FOR ITINERARY ACTIVITY ENDPOINTS - LIST
    ########################################################################

    def test_activity_list(self):
        """
        Test listing all itinerary activities when the user is authenticated.
        """
        view = ItineraryActivityViewSet.as_view({'get': 'list'})
        request = self.factory.get(f'/itineraries/{self.itinerary.id}/activities/all/')
        force_authenticate(request, user=self.user)
        response = view(request, itinerary_pk=self.itinerary.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

    def test_activity_list_as_member(self):
        """
        Test listing all itinerary activities as a member of the trip.
        """
        view = ItineraryActivityViewSet.as_view({'get': 'list'})
        request = self.factory.get(f'/itineraries/{self.itinerary.id}/activities/all/')
        force_authenticate(request, user=self.member_user)
        response = view(request, itinerary_pk=self.itinerary.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

    def test_activity_list_as_not_member(self):
        """
        Test listing all itinerary activities as a user not a member of the trip.
        """
        view = ItineraryActivityViewSet.as_view({'get': 'list'})
        request = self.factory.get(f'/itineraries/{self.itinerary.id}/activities/all/')
        force_authenticate(request, user=self.not_member_user)
        response = view(request, itinerary_pk=self.itinerary.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_activity_list_unauthenticated(self):
        """
        Test listing itinerary activities without authentication.
        """
        view = ItineraryActivityViewSet.as_view({'get': 'list'})
        request = self.factory.get('/activities/')
        response = view(request, itinerary_pk=self.itinerary.pk)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
