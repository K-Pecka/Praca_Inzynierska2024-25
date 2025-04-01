from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework import status

from trips.views.budget_views import BudgetUpdateAPIView, BudgetDestroyAPIView
from trips.views.expense_views import ExpenseCreateAPIView, ExpenseRetrieveAPIView, ExpenseUpdateAPIView, \
    ExpenseDestroyAPIView
from trips.views.ticket_views import TicketCreateAPIView, TicketRetrieveAPIView, TicketDestroyAPIView
from users.models import CustomUser, UserProfile
from trips.models import Trip, Budget, Expense, Ticket, TicketType, ExpenseType, Currency


class BudgetAPITestCase(TestCase):
    def setUp(self):
        """
        Set up the test data, including a user, their profile, a trip, and a budget.
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

        self.budget = Budget.objects.create(
            trip=self.trip,
            amount=1000.00,
            currency="USD"
        )

    def test_budget_update(self):
        """
        Test updating a budget when the user is authenticated.
        """
        data = {
            'amount': 1500.00,
            'currency': 'EUR'
        }
        view = BudgetUpdateAPIView.as_view()
        request = self.factory.patch(f'/trip/{self.trip.id}/budget/{self.budget.id}/update/', data)
        force_authenticate(request, user=self.user)
        response = view(request, trip_id=self.budget.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.budget.refresh_from_db()
        self.assertEqual(str(self.budget.amount), "1500.00")

    def test_budget_destroy(self):
        """
        Test deleting a budget.
        """
        view = BudgetDestroyAPIView.as_view()
        request = self.factory.delete(f'/trips/{self.trip.id}/budget/{self.budget.id}/delete/')
        force_authenticate(request, user=self.user)
        response = view(request, trip_id=self.trip.id, budget_id=self.budget.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Budget.objects.filter(id=self.budget.id).exists())


class ExpenseAPITestCase(TestCase):
    def setUp(self):
        """
        Set up the test data, including a user, their profile, a trip, a budget, and an expense.
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

        self.budget = Budget.objects.create(
            trip=self.trip,
            amount=3000.00,
            currency="USD"
        )
        self.currency = Currency.objects.create(code="USD")
        self.expense_category = ExpenseType.objects.create(name='food')
        self.expense = Expense.objects.create(
            trip=self.trip,
            user=self.user_profile,
            amount=200.00,
            title="Obiad w restauracji",
            currency=self.currency,
            date="2025-06-05",
            note="Obiad w dobrej restauracji",
            category=self.expense_category
        )

    def test_expense_create(self):
        """
        Test creating an expense when the request is valid.
        """
        data = {
            'trip': self.trip.id,
            'user': self.user_profile.id,
            'amount': 150.00,
            'title': "obiad smażalnia ryb",
            'currency': self.currency.id,
            'date': "2025-06-06",
            'note': "obiad w smażalni w złotych tarasach",
            'category': self.expense_category.id
        }
        view = ExpenseCreateAPIView.as_view()
        request = self.factory.post(f'/trips/{self.trip.id}/expense/', data)
        force_authenticate(request, user=self.user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_expense_retrieve(self):
        """
        Test retrieving an expense.
        """
        view = ExpenseRetrieveAPIView.as_view()
        request = self.factory.get(f'/trips/{self.trip.id}/expense/{self.expense.id}/')
        force_authenticate(request, user=self.user)
        response = view(request, pk=self.expense.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['amount'], "200.00")
        self.assertEqual(response.data['title'], "Obiad w restauracji")

    def test_expense_update(self):
        """
        Test updating an expense when the user is authenticated.
        """
        data = {
            'amount': 250.00,
            'title': "Obiad w barze",
            'note': "Obiad w jakimś dobrym barze",
            'category': self.expense_category.id
        }
        view = ExpenseUpdateAPIView.as_view()
        request = self.factory.patch(f'/trips/{self.trip.id}/expense/{self.expense.id}/update/', data)
        force_authenticate(request, user=self.user)
        response = view(request, pk=self.expense.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.expense.refresh_from_db()
        self.assertEqual(str(self.expense.amount), "250.00")
        self.assertEqual(self.expense.title, "Obiad w barze")

    def test_expense_destroy(self):
        """
        Test deleting an expense.
        """
        view = ExpenseDestroyAPIView.as_view()
        request = self.factory.delete(f'/trips/{self.trip.id}/expense/{self.expense.id}/delete/')
        force_authenticate(request, user=self.user)
        response = view(request, pk=self.expense.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Expense.objects.filter(id=self.expense.id).exists())

    def test_expense_create_unauthenticated(self):
        """
        Test creating an expense without authentication.
        """
        data = {
            'trip': self.trip.id,
            'user': self.user_profile.id,
            'amount': 100.00,
            'title': "Bilet do muzeum",
            'currency': self.currency.id,
            'date': "2025-06-07",
            'note': "Bilet do muzeum w paryżu",
            'category': self.expense_category.id
        }
        view = ExpenseCreateAPIView.as_view()
        request = self.factory.post(f'/trips/{self.trip.id}/expense/', data)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TicketAPITestCase(TestCase):
    def setUp(self):
        """
        Set up the test data, including a user, their profile, a trip, and a ticket type.
        """
        self.factory = APIRequestFactory()

        self.user = CustomUser.objects.create_user(
            email="testuser@example.com",
            password="TestPassword123",
            date_of_birth="19900101",
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

        self.ticket_type = TicketType.objects.create(name="Standard")

        self.ticket = Ticket.objects.create(
            file="tickets/sample.pdf",
            type=self.ticket_type,
            valid_from="2025-06-05T12:00:00Z",
            profile=self.user_profile,
            trip=self.trip
        )

    def test_ticket_create(self):
        """
        Test creating a ticket when the request is valid.
        """
        file = SimpleUploadedFile("new_ticket.pdf", b"file_content_here", content_type="application/pdf")
        data = {
            'file': file,
            'type': self.ticket_type.id,
            'valid_from': "2025-06-07T14:00:00Z",
            'profile': self.user_profile.id,
            'trip': self.trip.id
        }
        view = TicketCreateAPIView.as_view()
        request = self.factory.post(f'/trips/{self.trip.id}/tickets/', data)
        force_authenticate(request, user=self.user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_ticket_retrieve(self):
        """
        Test retrieving a ticket.
        """
        expected_url = f'http://testserver/{self.ticket.file.name}'

        view = TicketRetrieveAPIView.as_view()
        request = self.factory.get(f'/trips/{self.trip.id}/tickets/{self.ticket.id}/')
        force_authenticate(request, user=self.user)
        response = view(request, pk=self.ticket.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['file'], expected_url)


    # def test_ticket_update(self):
    #     """
    #     Test updating a ticket when the user is authenticated.
    #     """
    #     file = SimpleUploadedFile("new_ticket.pdf", b"file_content_here", content_type="application/pdf")
    #     data = {
    #         'file': file,
    #         'valid_from': "2025-06-08T10:00:00Z"
    #     }
    #     view = TicketUpdateAPIView.as_view()
    #     request = self.factory.patch(f'/trips/{self.trip.id}/tickets/{self.ticket.id}/update/', data)
    #     force_authenticate(request, user=self.user)
    #     response = view(request, pk=self.ticket.id)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #
    #     self.ticket.refresh_from_db()
    #
    #     self.assertEqual(self.ticket.file.name.startswith("tickets/new_ticket"), 'xd')

    def test_ticket_destroy(self):
        """
        Test deleting a ticket.
        """
        view = TicketDestroyAPIView.as_view()
        request = self.factory.delete(f'/trips/{self.trip.id}/tickets/{self.ticket.id}/delete/')
        force_authenticate(request, user=self.user)
        response = view(request, pk=self.ticket.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Ticket.objects.filter(id=self.ticket.id).exists())

    def test_ticket_create_unauthenticated(self):
        """
        Test creating a ticket without authentication.
        """
        data = {
            'file': "tickets/no_auth_ticket.pdf",
            'type': self.ticket_type.id,
            'valid_from': "2025-06-09T15:00:00Z",
            'profile': self.user_profile.id,
            'trip': self.trip.id
        }
        view = TicketCreateAPIView.as_view()
        request = self.factory.post(f'/trips/{self.trip.id}/tickets/', data)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

