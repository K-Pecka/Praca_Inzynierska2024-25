from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework import status

from chats.models import Chatroom, ChatMessage
from chats.views.chat_message_views import ChatMessageCreateAPIView, ChatMessageUpdateAPIView, \
    ChatMessageRetrieveAPIView, ChatMessageDestroyAPIView, ChatMessageListAPIView
from chats.views.chatroom_views import ChatroomDestroyAPIView, ChatroomListAPIView, ChatroomRetrieveAPIView, \
    ChatroomUpdateAPIView, ChatroomCreateAPIView
from users.models import CustomUser

from trips.models import Trip


class ChatAPITestCase(TestCase):
    def setUp(self):
        """
        Setup a test Chatroom, and set up URLs.
        """
        self.factory = APIRequestFactory()
        self.user = CustomUser.objects.create_user(
            email="jacob@…",
            password="Top_secret12",
            first_name="jacob",
            last_name="ereres",
            date_of_birth="1995-05-15"
        )
        self.user2 = CustomUser.objects.create_user(
            email="jacob2@…",
            password="Top_secret12",
            first_name="jacob",
            last_name="ereres",
            date_of_birth="1995-05-15"
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
        self.chat_message = ChatMessage.objects.create(
            text="test_chatmessage",
            profile=self.user_profile,
            chatroom=self.chatroom,
        )
        self.chat_message2 = ChatMessage.objects.create(
            text="test_chatmessage",
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
        view = ChatroomCreateAPIView.as_view()
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

        view = ChatroomCreateAPIView.as_view()
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

        view = ChatroomCreateAPIView.as_view()
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

        view = ChatroomUpdateAPIView.as_view()
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

        view = ChatroomUpdateAPIView.as_view()
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

        view = ChatroomUpdateAPIView.as_view()
        request = self.factory.patch(f'{self.chatroom.id}/', data, format='json')
        response = view(request, pk=self.chatroom.id)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_chatroom_delete(self):
        """
        Test deleting the chatroom.
        """
        view = ChatroomDestroyAPIView.as_view()
        request = self.factory.delete(f'{self.chatroom.id}/', format='json')
        force_authenticate(request, user=self.user)
        response = view(request, pk=self.chatroom.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_chatroom_not_creator_delete(self):
        """
        Test deleting the chatroom as a non-creator.
        """
        view = ChatroomDestroyAPIView.as_view()
        request = self.factory.delete(f'{self.chatroom2.id}/', format='json')
        force_authenticate(request, user=self.user)
        response = view(request, pk=self.chatroom2.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_chatroom_delete_unauthenticated(self):
        """
        Test deleting the chatroom when the user is not authenticated.
        """
        view = ChatroomDestroyAPIView.as_view()
        request = self.factory.delete(f'{self.chatroom.id}/', format='json')
        response = view(request, pk=self.chatroom.id)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_chatroom_retrieve(self):
        """
        Test retrieving the chatroom.
        """
        view = ChatroomRetrieveAPIView.as_view()
        request = self.factory.get(f'{self.chatroom.id}/', format='json')
        force_authenticate(request, user=self.user)
        response = view(request, pk=self.chatroom.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_chatroom_no_member_retrieve(self):
        """
        Test retrieving the chatroom as a non-member.
        """
        view = ChatroomRetrieveAPIView.as_view()
        request = self.factory.get(f'{self.chatroom2.id}/', format='json')
        force_authenticate(request, user=self.user)
        response = view(request, pk=self.chatroom2.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_chatroom_retrieve_unauthenticated(self):
        """
        Test retrieving the chatroom when the user is not authenticated.
        """
        view = ChatroomRetrieveAPIView.as_view()
        request = self.factory.get(f'{self.chatroom.id}/', format='json')
        response = view(request, pk=self.chatroom.id)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_chatroom_list(self):
        """
        Test retrieving list of the chatrooms.
        """
        view = ChatroomListAPIView.as_view()
        request = self.factory.get(f'all/', format='json')
        force_authenticate(request, user=self.user)
        response = view(request, pk=self.chatroom.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_chatroom_list_unauthenticated(self):
        """
        Test retrieving list of the chatrooms when the user is not authenticated.
        """
        view = ChatroomListAPIView.as_view()
        request = self.factory.get(f'all/', format='json')
        response = view(request, pk=self.chatroom.id)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # ChatMessage tests

    def test_chatmessage_no_file_create(self):
        """
        Test creating a chatmessage without file.
        """
        data = {
            'text': 'test_chatmessage',
            'profile': self.user_profile.id,
            'chatroom': self.chatroom.id
        }

        view = ChatMessageCreateAPIView.as_view()
        request = self.factory.post(f'chat/{self.chatroom.id}/chat-message/', data, format='json')
        force_authenticate(request, user=self.user)
        response = view(request, room_pk=self.chatroom.id)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_chatmessage_no_file_create_unauthenticated(self):
        """
        Test creating a chatmessage when the user is not authenticated.
        """
        data = {
            'text': 'test_chatmessage',
            'profile': self.user_profile.id,
            'chatroom': self.chatroom.id,
        }

        view = ChatMessageCreateAPIView.as_view()
        request = self.factory.post('chat/chat-message/', data, format='json')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_chatmessage_update(self):
        """
        Test updating the chatmessage.
        """
        data = {
            'text': 'test_chatmessage2',
            'profile': self.user_profile.id,
            'chatroom': self.chatroom.id,
        }

        view = ChatMessageUpdateAPIView.as_view()
        request = self.factory.patch(f'chat/{self.chat_message.id}/', data, format='json')
        force_authenticate(request, user=self.user)
        response = view(request, room_pk=self.chatroom.id, pk=self.chat_message.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_chatmessage_update_unauthenticated(self):
        """
        Test updating the chatmessage when the user is not authenticated.
        """
        data = {
            'text': 'test_chatmessage2',
            'profile': self.user_profile.id,
            'chatroom': self.chatroom.id,
        }

        view = ChatMessageUpdateAPIView.as_view()
        path = f'chat/{self.chatroom.id}/chat-message/{self.chat_message.id}/'
        request = self.factory.patch(path, data, format='json')
        response = view(request, room_pk=self.chatroom.id, pk=self.chat_message.id)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_chatmessage_delete(self):
        """
        Test deleting the chatmessage.
        """
        view = ChatroomDestroyAPIView.as_view()
        path = f'chat/{self.chatroom.id}/chat-message/{self.chat_message.id}/'
        request = self.factory.delete(path, format='json')
        force_authenticate(request, user=self.user)
        response = view(request, room_pk=self.chatroom.id, pk=self.chat_message.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_chatmessage_delete_unauthenticated(self):
        """
        Test deleting the chatmessage when the user is not authenticated.
        """
        view = ChatMessageDestroyAPIView.as_view()
        path = f'chat/{self.chatroom.id}/chat-message/{self.chat_message.id}/'
        request = self.factory.delete(path, format='json')
        response = view(request, room_pk=self.chatroom.id, pk=self.chat_message.id)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_chatmessage_retrieve(self):
        """
        Test retrieving the chatmessage.
        """
        view = ChatMessageRetrieveAPIView.as_view()
        path = f'chat/{self.chatroom.id}/chat-message/{self.chat_message.id}/'
        request = self.factory.get(path, format='json')
        force_authenticate(request, user=self.user)
        response = view(request, room_pk=self.chatroom.id, pk=self.chat_message.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_chatmessage_retrieve_unauthenticated(self):
        """
        Test retrieving the chatmessage when the user is not authenticated.
        """
        view = ChatMessageRetrieveAPIView.as_view()
        path = f'chat/{self.chatroom.id}/chat-message/{self.chat_message.id}/'
        request = self.factory.get(path, format='json')
        response = view(request, room_pk=self.chatroom.id, pk=self.chat_message.id)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_chatmessage_list(self):
        """
        Test retrieving list of the chatmessages.
        """
        view = ChatMessageListAPIView.as_view()
        path = f'chat/{self.chatroom.id}/chat-message/all/'
        request = self.factory.get(path, format='json')
        force_authenticate(request, user=self.user)
        response = view(request, room_pk=self.chatroom.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_chatmessage_list_unauthenticated(self):
        """
        Test retrieving list of the chatmessages when the user is not authenticated.
        """
        view = ChatMessageListAPIView.as_view()
        path = f'chat/{self.chatroom.id}/chat-message/all/'
        request = self.factory.get(path, format='json')
        response = view(request, room_pk=self.chatroom.id)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
