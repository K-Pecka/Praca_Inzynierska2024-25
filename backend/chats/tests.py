from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework import status

from chats.models import Chatroom, Message
from chats.views.chatroom_views import ChatroomViewSet
from chats.views.message_views import MessageViewSet

from users.models import CustomUser, UserProfileType

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
            email="jacob@…",
            password="Top_secret12",
            first_name="jacob",
            last_name="ereres",
        )
        self.user2 = CustomUser.objects.create_user(
            email="jacob2@…",
            password="Top_secret12",
            first_name="jacob",
            last_name="ereres",
        )
        self.user_profile = self.user.get_default_profile()
        self.user_profile2 = self.user2.get_default_profile()
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
            creator=self.user_profile2,
            settings={"currency": "USD", "guide_price": 1000.00},
            start_date="2025-06-01",
            end_date="2025-06-10"
        )
        self.trip2.members.add(self.user_profile2)
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
            creator=self.user_profile2,
            settings={"currency": "USD"}
        )
        self.message = Message.objects.create(
            content="test_message",
            profile=self.user_profile,
            chatroom=self.chatroom,
        )
        self.message2 = Message.objects.create(
            content="test_message",
            profile=self.user_profile2,
            chatroom=self.chatroom2,
        )

    # Chatroom tests

    def test_chatroom_create(self):
        """
        Test creating a chatroom when the request is valid.
        """
        data = {
            'name': 'test_chatroom',
            'type': 'Prywatny',
            'members': [self.user_profile.id],
            'settings': {'currency': 'USD'}
        }
        view = ChatroomViewSet.as_view({'post': 'create'})
        request = self.factory.post(f'trip/1/chat/', data, format='json')
        force_authenticate(request, user=self.user)
        response = view(request, trip_pk=1, itinerary_pk=1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

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
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_chatroom_update(self):
        """
        Test updating the chatroom.
        """
        data = {
            'name': 'test_chatroom',
            'type': 'Prywatny',
            'trip': self.trip.id,
            'creator': self.user_profile.id,
            'members': [self.user_profile2.id],
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
            'creator': self.user_profile2.id,
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
            'members': [self.user_profile2.id],
            'settings': {'currency': 'USD'}
        }

        view = ChatroomViewSet.as_view({'patch': 'partial_update'})
        request = self.factory.patch(f'{self.chatroom.id}/', data, format='json')
        response = view(request, pk=self.chatroom.id)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_chatroom_delete(self):
        """
        Test deleting the chatroom.
        """
        view = ChatroomViewSet.as_view({'delete': 'destroy'})
        request = self.factory.delete(f'{self.chatroom.id}/', format='json')
        force_authenticate(request, user=self.user)
        response = view(request, pk=self.chatroom.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_chatroom_not_creator_delete(self):
        """
        Test deleting the chatroom as a non-creator.
        """
        view = ChatroomViewSet.as_view({'delete': 'destroy'})
        request = self.factory.delete(f'{self.chatroom2.id}/', format='json')
        force_authenticate(request, user=self.user)
        response = view(request, pk=self.chatroom2.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_chatroom_delete_unauthenticated(self):
        """
        Test deleting the chatroom when the user is not authenticated.
        """
        view = ChatroomViewSet.as_view({'delete': 'destroy'})
        request = self.factory.delete(f'{self.chatroom.id}/', format='json')
        response = view(request, pk=self.chatroom.id)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

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

    # Message tests

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

    def test_message_delete(self):
        """
        Test deleting the message.
        """
        view = MessageViewSet.as_view({'delete': 'destroy'})
        path = f'chat/{self.chatroom.id}/chat-message/{self.message.id}/'
        request = self.factory.delete(path, format='json')
        force_authenticate(request, user=self.user)
        response = view(request, room_pk=self.chatroom.id, pk=self.message.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_message_delete_unauthenticated(self):
        """
        Test deleting the message when the user is not authenticated.
        """
        view = MessageViewSet.as_view({'delete': 'destroy'})
        path = f'chat/{self.chatroom.id}/chat-message/{self.message.id}/'
        request = self.factory.delete(path, format='json')
        response = view(request, room_pk=self.chatroom.id, pk=self.message.id)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

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
