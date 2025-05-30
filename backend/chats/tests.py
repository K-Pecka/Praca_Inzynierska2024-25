from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework import status

from chats.models import Chatroom, Message
from chats.views.chatroom_views import ChatroomViewSet
from chats.views.message_views import MessageViewSet

from users.models import CustomUser, UserProfileType, UserProfile

from trips.models import Trip


class ChatAPITestCase(TestCase):
    def setUp(self):
        """
        Setup a test Chatroom, and set up URLs.
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
            name="test_trip",
            creator=self.user_profile,
            settings={"currency": "USD", "guide_price": 1000.00},
            start_date="2025-06-01",
            end_date="2025-06-10"
        )
        self.trip.members.add(self.user_profile)
        self.trip2 = Trip.objects.create(
            name="test_trip2",
            creator=self.user_profile,
            settings={"currency": "USD", "guide_price": 1000.00},
            start_date="2025-06-01",
            end_date="2025-06-10"
        )
        self.trip2.members.add(self.member_user_profile)
        self.chatroom = Chatroom.objects.create(
            name="test_chatroom",
            type="Prywatny",
            trip=self.trip,
            creator=self.user_profile,
            settings={"currency": "USD"}
        )
        self.chatroom2 = Chatroom.objects.create(
            name="test_chatroom2",
            type="Prywatny",
            trip=self.trip2,
            creator=self.member_user_profile,
            settings={"currency": "USD"}
        )
        self.message = Message.objects.create(
            content="test_message",
            profile=self.user_profile,
            chatroom=self.chatroom,
        )
        self.message2 = Message.objects.create(
            content="test_message",
            profile=self.member_user_profile,
            chatroom=self.chatroom2,
        )

    ########################################################################
    # TEST CASES FOR CHATROOM ENDPOINTS - CREATE
    ########################################################################

    def test_chatroom_create_for_trip_creator(self):
        """
        Test creating a chatroom when the request is valid.
        """
        data = {
            'name': 'test_chatroom',
            'type': 'Prywatny',
            'trip': self.trip.id,
            'creator': self.user_profile.id,
            'settings': {'currency': 'USD'}
        }

        view = ChatroomViewSet.as_view({'post': 'create'})
        request = self.factory.post('chat/', data, format='json')
        force_authenticate(request, user=self.user)
        response = view(request, trip_pk=1, itinerary_pk=1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_chatroom_create_for_trip_member(self):
        """
        Test creating a chatroom when the user is a member of the trip.
        """
        data = {
            'name': 'test_chatroom',
            'type': 'Prywatny',
            'trip': self.trip.id,
            'creator': self.member_user_profile.id,
            'settings': {'currency': 'USD'}
        }

        view = ChatroomViewSet.as_view({'post': 'create'})
        request = self.factory.post('chat/', data, format='json')
        force_authenticate(request, user=self.member_user)
        response = view(request, trip_pk=1, itinerary_pk=1)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_chatroom_create_unauthenticated(self):
        """
        Test creating a chatroom when the user is not authenticated.
        """
        data = {
            'name': 'test_chatroom',
            'type': 'Prywatny',
            'trip': self.trip.id,
            'creator': self.user_profile.id,
            'settings': {'currency': 'USD'}
        }

        view = ChatroomViewSet.as_view({'post': 'create'})
        request = self.factory.post('chat/', data, format='json')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_chatroom_duplicate_members_create(self):
        """
        Test creating a chatroom when there are duplicated members in request data.
        """
        data = {
            'name': 'test_chatroom',
            'type': 'Prywatny',
            'trip': self.trip.id,
            'members': [self.user_profile.id, self.user_profile.id],
            'creator': self.user_profile.id,
            'settings': {'currency': 'USD'}
        }

        view = ChatroomViewSet.as_view({'post': 'create'})
        request = self.factory.post('chat/', data, format='json')
        force_authenticate(request, user=self.user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    ########################################################################
    # TEST CASES FOR CHATROOM ENDPOINTS - UPDATE
    ########################################################################

    def test_chatroom_update_as_creator(self):
        """
        Test updating the chatroom.
        """
        data = {
            'name': 'test_chatroom',
            'type': 'Prywatny',
            'trip': self.trip.id,
            'creator': self.user_profile.id,
            'members': [self.member_user.id],
            'settings': {'currency': 'USD'}
        }

        view = ChatroomViewSet.as_view({'patch': 'partial_update'})
        request = self.factory.patch(f'{self.chatroom.id}/', data, format='json')
        force_authenticate(request, user=self.user)
        response = view(request, pk=self.chatroom.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_chatroom_not_creator_update(self):
        """
        Test updating the chatroom as a non-creator.
        """
        data = {
            'name': 'test_chatroom',
            'type': 'Prywatny',
            'trip': self.trip2.id,
            'creator': self.member_user.id,
            'members': [self.user_profile.id],
            'settings': {'currency': 'USD'}
        }

        view = ChatroomViewSet.as_view({'patch': 'partial_update'})
        request = self.factory.patch(f'{self.chatroom2.id}/', data, format='json')
        force_authenticate(request, user=self.user)
        response = view(request, pk=self.chatroom2.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_chatroom_update_unauthenticated(self):
        """
        Test updating the chatroom when the user is not authenticated.
        """
        data = {
            'name': 'test_chatroom',
            'type': 'Prywatny',
            'trip': self.trip.id,
            'creator': self.user_profile.id,
            'members': [self.member_user.id],
            'settings': {'currency': 'USD'}
        }

        view = ChatroomViewSet.as_view({'patch': 'partial_update'})
        request = self.factory.patch(f'{self.chatroom.id}/', data, format='json')
        response = view(request, pk=self.chatroom.id)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    ########################################################################
    # TEST CASES FOR CHATROOM ENDPOINTS - DESTROY
    ########################################################################

    def test_chatroom_destroy_as_creator(self):
        """
        Test deleting the chatroom.
        """
        view = ChatroomViewSet.as_view({'delete': 'destroy'})
        request = self.factory.delete(f'{self.chatroom.id}/', format='json')
        force_authenticate(request, user=self.user)
        response = view(request, pk=self.chatroom.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_chatroom_not_creator_destroy(self):
        """
        Test deleting the chatroom as a non-creator.
        """
        view = ChatroomViewSet.as_view({'delete': 'destroy'})
        request = self.factory.delete(f'{self.chatroom2.id}/', format='json')
        force_authenticate(request, user=self.user)
        response = view(request, pk=self.chatroom2.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_chatroom_destroy_unauthenticated(self):
        """
        Test deleting the chatroom when the user is not authenticated.
        """
        view = ChatroomViewSet.as_view({'delete': 'destroy'})
        request = self.factory.delete(f'{self.chatroom.id}/', format='json')
        response = view(request, pk=self.chatroom.id)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    ########################################################################
    # TEST CASES FOR CHATROOM ENDPOINTS - RETRIEVE
    ########################################################################

    def test_chatroom_retrieve(self):
        """
        Test retrieving the chatroom.
        """
        view = ChatroomViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get(f'{self.chatroom.id}/', format='json')
        force_authenticate(request, user=self.user)
        response = view(request, pk=self.chatroom.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_chatroom_no_member_retrieve(self):
        """
        Test retrieving the chatroom as a non-member.
        """
        view = ChatroomViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get(f'{self.chatroom2.id}/', format='json')
        force_authenticate(request, user=self.user)
        response = view(request, pk=self.chatroom2.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_chatroom_retrieve_unauthenticated(self):
        """
        Test retrieving the chatroom when the user is not authenticated.
        """
        view = ChatroomViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get(f'{self.chatroom.id}/', format='json')
        response = view(request, pk=self.chatroom.id)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    ########################################################################
    # TEST CASES FOR CHATROOM ENDPOINTS - LIST
    ########################################################################

    def test_chatroom_list(self):
        """
        Test retrieving list of the chatrooms.
        """
        view = ChatroomViewSet.as_view({'get': 'list'})
        request = self.factory.get(f'all/', format='json')
        force_authenticate(request, user=self.user)
        response = view(request, pk=self.chatroom.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_chatroom_list_unauthenticated(self):
        """
        Test retrieving list of the chatrooms when the user is not authenticated.
        """
        view = ChatroomViewSet.as_view({'get': 'list'})
        request = self.factory.get(f'all/', format='json')
        response = view(request, pk=self.chatroom.id)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    ########################################################################
    # TEST CASES FOR MESSAGE ENDPOINTS - CREATE
    ########################################################################

    def test_message_no_file_create(self):
        """
        Test creating a message without file.
        """
        data = {
            'content': 'test_message',
            'profile': self.user_profile.id,
            'chatroom': self.chatroom.id
        }

        view = MessageViewSet.as_view({'post': 'create'})
        request = self.factory.post(f'chat/{self.chatroom.id}/chat-message/', data, format='json')
        force_authenticate(request, user=self.user)
        response = view(request, room_pk=self.chatroom.id)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_message_no_file_create_unauthenticated(self):
        """
        Test creating a message when the user is not authenticated.
        """
        data = {
            'content': 'test_message',
            'profile': self.user_profile.id,
            'chatroom': self.chatroom.id,
        }

        view = MessageViewSet.as_view({'post': 'create'})
        request = self.factory.post('chat/chat-message/', data, format='json')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    ########################################################################
    # TEST CASES FOR MESSAGE ENDPOINTS - UPDATE
    ########################################################################

    def test_message_update(self):
        """
        Test updating the message.
        """
        data = {
            'content': 'test_message2',
            'profile': self.user_profile.id,
            'chatroom': self.chatroom.id,
        }

        view = MessageViewSet.as_view({'patch': 'partial_update'})
        request = self.factory.patch(f'chat/{self.message.id}/', data, format='json')
        force_authenticate(request, user=self.user)
        response = view(request, room_pk=self.chatroom.id, pk=self.message.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_message_update_unauthenticated(self):
        """
        Test updating the message when the user is not authenticated.
        """
        data = {
            'content': 'test_message2',
            'profile': self.user_profile.id,
            'chatroom': self.chatroom.id,
        }

        view = MessageViewSet.as_view({'patch': 'partial_update'})
        path = f'chat/{self.chatroom.id}/chat-message/{self.message.id}/'
        request = self.factory.patch(path, data, format='json')
        response = view(request, room_pk=self.chatroom.id, pk=self.message.id)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    ########################################################################
    # TEST CASES FOR MESSAGE ENDPOINTS - DESTROY
    ########################################################################

    def test_message_destroy(self):
        """
        Test deleting the message.
        """
        view = MessageViewSet.as_view({'delete': 'destroy'})
        path = f'chat/{self.chatroom.id}/chat-message/{self.message.id}/'
        request = self.factory.delete(path, format='json')
        force_authenticate(request, user=self.user)
        response = view(request, room_pk=self.chatroom.id, pk=self.message.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_message_destroy_unauthenticated(self):
        """
        Test deleting the message when the user is not authenticated.
        """
        view = MessageViewSet.as_view({'delete': 'destroy'})
        path = f'chat/{self.chatroom.id}/chat-message/{self.message.id}/'
        request = self.factory.delete(path, format='json')
        response = view(request, room_pk=self.chatroom.id, pk=self.message.id)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    ########################################################################
    # TEST CASES FOR MESSAGE ENDPOINTS - RETRIEVE
    ########################################################################

    def test_message_retrieve(self):
        """
        Test retrieving the message.
        """
        view = MessageViewSet.as_view({'get': 'retrieve'})
        path = f'chat/{self.chatroom.id}/chat-message/{self.message.id}/'
        request = self.factory.get(path, format='json')
        force_authenticate(request, user=self.user)
        response = view(request, room_pk=self.chatroom.id, pk=self.message.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_message_retrieve_unauthenticated(self):
        """
        Test retrieving the chatmessage when the user is not authenticated.
        """
        view = MessageViewSet.as_view({'get': 'retrieve'})
        path = f'chat/{self.chatroom.id}/chat-message/{self.message.id}/'
        request = self.factory.get(path, format='json')
        response = view(request, room_pk=self.chatroom.id, pk=self.message.id)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    ########################################################################
    # TEST CASES FOR MESSAGE ENDPOINTS - LIST
    ########################################################################

    def test_message_list(self):
        """
        Test retrieving list of the chatmessages.
        """
        view = MessageViewSet.as_view({'get': 'list'})
        path = f'chat/{self.chatroom.id}/chat-message/all/'
        request = self.factory.get(path, format='json')
        force_authenticate(request, user=self.user)
        response = view(request, room_pk=self.chatroom.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_message_list_unauthenticated(self):
        """
        Test retrieving list of the chatmessages when the user is not authenticated.
        """
        view = MessageViewSet.as_view({'get': 'list'})
        path = f'chat/{self.chatroom.id}/chat-message/all/'
        request = self.factory.get(path, format='json')
        response = view(request, room_pk=self.chatroom.id)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
