from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework import status
from django.core.files.storage import FileSystemStorage
from django.test.utils import override_settings

from trips.views.expense_views import ExpenseViewSet
from trips.views.ticket_views import TicketViewSet
from users.models import CustomUser, UserProfile, UserProfileType
from trips.models import Trip, Expense, Ticket, TicketType, ExpenseType


class ExpenseAPITestCase(TestCase):
    def setUp(self):
        """
        Set up the test data, including a user, their profile, a trip, a budget, and an expense.
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
        self.trip.save()
        self.expense_category = ExpenseType.objects.create(name='food')
        self.expense = Expense.objects.create(
            trip=self.trip,
            user=self.user_profile,
            amount=200.00,
            title="Obiad w restauracji",
            currency='USD',
            date="2025-06-05",
            note="Obiad w dobrej restauracji",
            category=self.expense_category
        )

    ########################################################################
    # TEST CASES FOR EXPENSE ENDPOINTS - CREATE
    ########################################################################

    def test_expense_create_as_creator(self):
        """
        Test creating an expense when the request is valid.
        """
        data = {
            'title': "obiad smażalnia ryb",
            'user': self.user_profile.id,
            'amount': 150.00,
            'currency': "USD",
            'date': "06.06.2025",
            'category': self.expense_category.id
        }
        view = ExpenseViewSet.as_view({'post': 'create'})
        request = self.factory.post(f'/trips/{self.trip.id}/expense/', data)
        force_authenticate(request, user=self.user)
        response = view(request, trip_pk=self.trip.id)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_expense_create_as_not_member(self):
        """
        Test creating an expense as a user who is not a member of the trip.
        """
        data = {
            'title': "obiad smażalnia ryb",
            'user': self.not_member_user_profile.id,
            'amount': 150.00,
            'currency': "USD",
            'date': "06.06.2025",
            'category': self.expense_category.id
        }
        view = ExpenseViewSet.as_view({'post': 'create'})
        request = self.factory.post(f'/trips/{self.trip.id}/expense/', data)
        force_authenticate(request, user=self.not_member_user)
        response = view(request, trip_pk=self.trip.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_expense_create_unauthenticated(self):
        """
        Test creating an expense without authentication.
        """
        data = {
            'trip': self.trip.id,
            'user': self.user_profile.id,
            'amount': 100.00,
            'title': "Bilet do muzeum",
            'currency': "USD",
            'date': "2025-06-07",
            'note': "Bilet do muzeum w paryżu",
            'category': self.expense_category.id
        }
        view = ExpenseViewSet.as_view({'post': 'create'})
        request = self.factory.post(f'/trips/{self.trip.id}/expense/', data)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    ########################################################################
    # TEST CASES FOR EXPENSE ENDPOINTS - RETRIEVE
    ########################################################################

    def test_expense_retrieve_as_creator(self):
        """
        Test retrieving an expense.
        """
        view = ExpenseViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get(f'/trips/{self.trip.id}/expense/{self.expense.id}/')
        force_authenticate(request, user=self.user)
        response = view(request, trip_pk=self.trip.id, pk=self.expense.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['amount'], "200.00")
        self.assertEqual(response.data['title'], "Obiad w restauracji")

    def test_expense_retrieve_as_member(self):
        """
        Test retrieving an expense as a member of the trip.
        """
        view = ExpenseViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get(f'/trips/{self.trip.id}/expense/{self.expense.id}/')
        force_authenticate(request, user=self.member_user)
        response = view(request, trip_pk=self.trip.id, pk=self.expense.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['amount'], "200.00")
        self.assertEqual(response.data['title'], "Obiad w restauracji")

    def test_expense_retrieve_as_not_member(self):
        """
        Test retrieving an expense as a user who is not a member of the trip.
        """
        view = ExpenseViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get(f'/trips/{self.trip.id}/expense/{self.expense.id}/')
        force_authenticate(request, user=self.not_member_user)
        response = view(request, trip_pk=self.trip.id, pk=self.expense.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    ########################################################################
    # TEST CASES FOR EXPENSE ENDPOINTS - UPDATE
    ########################################################################

    def test_expense_update_as_creator(self):
        """
        Test updating an expense when the user is authenticated.
        """
        data = {
            'amount': 250.00,
            'title': "Obiad w barze",
            'note': "Obiad w jakimś dobrym barze",
            'category': self.expense_category.id
        }
        view = ExpenseViewSet.as_view({'patch': 'partial_update'})
        request = self.factory.patch(f'/trips/{self.trip.id}/expense/{self.expense.id}/update/', data)
        force_authenticate(request, user=self.user)
        response = view(request, trip_pk=self.trip.id, pk=self.expense.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.expense.refresh_from_db()
        self.assertEqual(str(self.expense.amount), "250.00")
        self.assertEqual(self.expense.title, "Obiad w barze")

    def test_expense_update_as_member(self):
        """
        Test updating an expense as a member of the trip.
        """
        data = {
            'amount': 250.00,
            'title': "Obiad w barze",
            'note': "Obiad w jakimś dobrym barze",
            'category': self.expense_category.id
        }
        view = ExpenseViewSet.as_view({'patch': 'partial_update'})
        request = self.factory.patch(f'/trips/{self.trip.id}/expense/{self.expense.id}/update/', data)
        force_authenticate(request, user=self.member_user)
        response = view(request, trip_pk=self.trip.id, pk=self.expense.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.expense.refresh_from_db()
        self.assertEqual(str(self.expense.amount), "200.00")
        self.assertEqual(self.expense.title, "Obiad w restauracji")

    def test_expense_update_as_not_member(self):
        """
        Test updating an expense as a user who is not a member of the trip.
        """
        data = {
            'amount': 250.00,
            'title': "Obiad w barze",
            'note': "Obiad w jakimś dobrym barze",
            'category': self.expense_category.id
        }
        view = ExpenseViewSet.as_view({'patch': 'partial_update'})
        request = self.factory.patch(f'/trips/{self.trip.id}/expense/{self.expense.id}/update/', data)
        force_authenticate(request, user=self.not_member_user)
        response = view(request, trip_pk=self.trip.id, pk=self.expense.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    ########################################################################
    # TEST CASES FOR EXPENSE ENDPOINTS - DESTROY
    ########################################################################

    def test_expense_destroy(self):
        """
        Test deleting an expense.
        """
        view = ExpenseViewSet.as_view({'delete': 'destroy'})
        request = self.factory.delete(f'/trips/{self.trip.id}/expense/{self.expense.id}/delete/')
        force_authenticate(request, user=self.user)
        response = view(request, trip_pk=self.trip.id, pk=self.expense.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Expense.objects.filter(id=self.expense.id).exists())


@override_settings(
    DEFAULT_FILE_STORAGE="django.core.files.storage.FileSystemStorage"
)
class TicketAPITestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

        # Typ profilu
        self.default_user_profile_type, _ = UserProfileType.objects.get_or_create(
            code="tourist",
            defaults={"name": "Tourist"}
        )

        # Użytkownik
        self.user = CustomUser.objects.create_user(
            email="testuser@example.com",
            password="TestPassword123",
            first_name="Test",
            last_name="User",
        )

        self.user_profile, _ = UserProfile.objects.get_or_create(
            user=self.user,
            defaults={"type": self.default_user_profile_type}
        )

        # Wycieczka
        self.trip = Trip.objects.create(
            creator=self.user_profile,
            settings={"currency": "USD"},
            start_date="2025-06-01",
            end_date="2025-06-15"
        )
        self.trip.members.add(self.user_profile)

        # Typ biletu
        self.ticket_type = TicketType.objects.create(name="Standard")
        Ticket._meta.get_field('file').storage = FileSystemStorage()

        self.ticket = Ticket.objects.create(
            file=SimpleUploadedFile("sample.pdf", b"test content", content_type="application/pdf"),
            type=self.ticket_type,
            valid_from_date="2025-06-05",
            valid_from_time="12:00",
            owner=self.user_profile,
            trip=self.trip
        )
        self.ticket.profiles.add(self.user_profile)

    def test_ticket_create(self):
        file = SimpleUploadedFile("ticket.pdf", b"filecontent", content_type="application/pdf")
        data = {
            "file": file,
            "type": self.ticket_type.id,
            "valid_from_date": "2025-06-07",
            "valid_from_time": "14:00",
            "trip": self.trip.id,
        }
        view = TicketViewSet.as_view({'post': 'create'})
        request = self.factory.post('/trip/ticket/create/', data, format='multipart')
        force_authenticate(request, user=self.user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_ticket_retrieve(self):
        view = TicketViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get(f'/trip/ticket/{self.ticket.id}/')
        force_authenticate(request, user=self.user)
        response = view(request, trip_pk=self.trip.pk, pk=self.ticket.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['trip'], self.trip.id)

    def test_ticket_update(self):
        file = SimpleUploadedFile("updated.pdf", b"new content", content_type="application/pdf")
        data = {
            "file": file,
            "type": self.ticket_type.id,
            "valid_from_date": "2025-06-08",
            "valid_from_time": "16:00"
        }
        view = TicketViewSet.as_view({'patch': 'partial_update'})
        request = self.factory.patch(f'/trip/ticket/{self.ticket.id}/update/', data, format='multipart')
        force_authenticate(request, user=self.user)
        response = view(request, trip_pk=self.trip.pk, pk=self.ticket.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_ticket_destroy(self):
        view = TicketViewSet.as_view({'delete': 'destroy'})
        request = self.factory.delete(f'/trip/ticket/{self.ticket.id}/delete/')
        force_authenticate(request, user=self.user)
        response = view(request, trip_pk=self.trip.pk, pk=self.ticket.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Ticket.objects.filter(id=self.ticket.id).exists())

    def test_ticket_create_unauthenticated(self):
        file = SimpleUploadedFile("unauth.pdf", b"unauth", content_type="application/pdf")
        data = {
            "file": file,
            "type": self.ticket_type.id,
            "valid_from_date": "2025-06-09",
            "valid_from_time": "15:00",
            "trip": self.trip.id,
        }
        view = TicketViewSet.as_view({'post': 'create'})
        request = self.factory.post('/trip/ticket/create/', data, format='multipart')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def tearDown(self):
        self.ticket.file.delete(save=False)
