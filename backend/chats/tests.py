from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status
from rest_framework.test import force_authenticate

from chats.models import Chatroom, ChatMessage
from users.models import CustomUser

from trips.models import Trip

from chats.api_views import ChatroomCreateAPIView, ChatroomUpdateAPIView, ChatroomDestroyAPIView, \
    ChatroomRetrieveAPIView, ChatroomListAPIView, ChatMessageCreateAPIView, ChatMessageUpdateAPIView, \
    ChatMessageRetrieveAPIView, ChatMessageDestroyAPIView, ChatMessageListAPIView

from users.models import UserProfile


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
        self.trip = Trip.objects.create(
            creator=self.user.profile,
            budget=1000.00,
            settings={"currency": "USD", "guide_price": 1000.00},
            start_date="2025-06-01",
            end_date="2025-06-10"
        )
        self.user_profile = self.user.profile
        self.chatroom = Chatroom.objects.create(
            name="test_chatroom2",
            type="Prywatny",
            trip=self.trip,
            guide=self.user.profile,
            settings={"currency": "USD"}
        )
        self.chat_message = ChatMessage.objects.create(
            text="test_chatmessage",
            profile=self.user.profile,
            chatroom=self.chatroom,
        )


    # Chatroom tests

    # def test_chatroom_create(self):
    #     """
    #     Test creating a chatroom when the request is valid.
    #     """
    #     data = {
    #         'name': 'test_chatroom',
    #         'type': 'Prywatny',
    #         'trip': self.trip.id,
    #         'guide': self.user_profile.id,
    #         'settings': {'currency': 'USD'}
    #     }
    #
    #     view = ChatroomCreateAPIView.as_view()
    #     request = self.factory.post('chat/', data, format='json')
    #     force_authenticate(request, user=self.user)
    #     response = view(request)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #
    #
    # def test_chatroom_create_unauthenticated(self):
    #     """
    #     Test creating a chatroom when the user is not authenticated.
    #     """
    #     data = {
    #         'name': 'test_chatroom',
    #         'type': 'Prywatny',
    #         'trip': self.trip.id,
    #         'guide': self.user_profile.id,
    #         'settings': {'currency': 'USD'}
    #     }
    #
    #     view = ChatroomCreateAPIView.as_view()
    #     request = self.factory.post('chat/', data, format='json')
    #     response = view(request)
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    #
    #
    # def test_chatroom_duplicate_tourists_create(self):
    #     """
    #     Test creating a chatroom when there are duplicated tourists in request data.
    #     """
    #     data = {
    #         'name': 'test_chatroom',
    #         'type': 'Prywatny',
    #         'trip': self.trip.id,
    #         'tourists': [self.user_profile.id, self.user_profile.id],
    #         'guide': self.user_profile.id,
    #         'settings': {'currency': 'USD'}
    #     }
    #
    #     view = ChatroomCreateAPIView.as_view()
    #     request = self.factory.post('chat/', data, format='json')
    #     force_authenticate(request, user=self.user)
    #     response = view(request)
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #
    #
    # def test_chatroom_update(self):
    #     """
    #     Test updating the chatroom.
    #     """
    #     data = {
    #         'name': 'test_chatroom',
    #         'type': 'Prywatny',
    #         'trip': self.trip.id,
    #         'guide': self.user_profile.id,
    #         'tourists': [self.user_profile.id],
    #         'settings': {'currency': 'USD'}
    #     }
    #
    #     view = ChatroomUpdateAPIView.as_view()
    #     request = self.factory.patch(f'{self.chatroom.id}/', data, format='json')
    #     force_authenticate(request, user=self.user)
    #     response = view(request, pk=self.chatroom.id)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #
    #
    # def test_chatroom_update_unauthenticated(self):
    #     """
    #     Test updating the chatroom when the user is not authenticated.
    #     """
    #     data = {
    #         'name': 'test_chatroom',
    #         'type': 'Prywatny',
    #         'trip': self.trip.id,
    #         'guide': self.user_profile.id,
    #         'tourists': [self.user_profile.id],
    #         'settings': {'currency': 'USD'}
    #     }
    #
    #     view = ChatroomUpdateAPIView.as_view()
    #     request = self.factory.patch(f'{self.chatroom.id}/', data, format='json')
    #     response = view(request, pk=self.chatroom.id)
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    #
    # def test_chatroom_delete(self):
    #     """
    #     Test deleting the chatroom.
    #     """
    #     view = ChatroomDestroyAPIView.as_view()
    #     request = self.factory.delete(f'{self.chatroom.id}/', format='json')
    #     force_authenticate(request, user=self.user)
    #     response = view(request, pk=self.chatroom.id)
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    #
    #
    # def test_chatroom_delete_unauthenticated(self):
    #     """
    #     Test deleting the chatroom when the user is not authenticated.
    #     """
    #     view = ChatroomDestroyAPIView.as_view()
    #     request = self.factory.delete(f'{self.chatroom.id}/', format='json')
    #     response = view(request, pk=self.chatroom.id)
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    #
    #
    # def test_chatroom_retrieve(self):
    #     """
    #     Test retrieving the chatroom.
    #     """
    #     view = ChatroomRetrieveAPIView.as_view()
    #     request = self.factory.get(f'{self.chatroom.id}/', format='json')
    #     force_authenticate(request, user=self.user)
    #     response = view(request, pk=self.chatroom.id)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #
    #
    # def test_chatroom_retrieve_unauthenticated(self):
    #     """
    #     Test retrieving the chatroom when the user is not authenticated.
    #     """
    #     view = ChatroomRetrieveAPIView.as_view()
    #     request = self.factory.get(f'{self.chatroom.id}/', format='json')
    #     response = view(request, pk=self.chatroom.id)
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    #
    #
    # def test_chatroom_list(self):
    #     """
    #     Test retrieving list of the chatrooms.
    #     """
    #     view = ChatroomListAPIView.as_view()
    #     request = self.factory.get(f'all/', format='json')
    #     force_authenticate(request, user=self.user)
    #     response = view(request, pk=self.chatroom.id)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #
    #
    # def test_chatroom_list_unauthenticated(self):
    #     """
    #     Test retrieving list of the chatrooms when the user is not authenticated.
    #     """
    #     view = ChatroomListAPIView.as_view()
    #     request = self.factory.get(f'all/', format='json')
    #     response = view(request, pk=self.chatroom.id)
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # ChatMessage tests

    def test_chatmessage_no_file_create(self):
        """
        Test creating a chatmessage without file.
        """
        data = {
            'text': 'test_chatmessage',
            'profile': self.user_profile.id,
            'chatroom': self.chatroom.id,
        }

        view = ChatMessageCreateAPIView.as_view()
        request = self.factory.post('chat/chat-message/', data, format='json')
        force_authenticate(request, user=self.user)
        response = view(request)
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
