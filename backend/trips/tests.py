from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework import status

from trips.api_views import BudgetUpdateAPIView, BudgetDestroyAPIView, \
    ExpenseUpdateAPIView, ExpenseDestroyAPIView, ExpenseRetrieveAPIView, ExpenseCreateAPIView
from users.models import CustomUser, UserProfile
from trips.models import Trip, Budget, Expense


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

        self.expense = Expense.objects.create(
            trip=self.trip,
            user=self.user_profile,
            amount=200.00,
            date="2025-06-05",
            description="Lunch at a restaurant",
            type="food"
        )

    def test_expense_create(self):
        """
        Test creating an expense when the request is valid.
        """
        data = {
            'trip': self.trip.id,
            'user': self.user_profile.id,
            'amount': 150.00,
            'date': "2025-06-06",
            'description': "Taxi fare",
            'type': "transport"
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

    def test_expense_update(self):
        """
        Test updating an expense when the user is authenticated.
        """
        data = {
            'amount': 250.00,
            'description': "Updated lunch cost",
            'type': "food"
        }
        view = ExpenseUpdateAPIView.as_view()
        request = self.factory.patch(f'/trips/{self.trip.id}/expense/{self.expense.id}/update/', data)
        force_authenticate(request, user=self.user)
        response = view(request, pk=self.expense.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.expense.refresh_from_db()
        self.assertEqual(str(self.expense.amount), "250.00")

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
            'budget': self.budget.id,
            'user': self.user_profile.id,
            'amount': 100.00,
            'date': "2025-06-07",
            'description': "Museum ticket",
            'type': "other"
        }
        view = ExpenseCreateAPIView.as_view()
        request = self.factory.post(f'/trips/{self.trip.id}/expense/', data)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
