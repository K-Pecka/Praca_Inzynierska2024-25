from django.contrib import admin

from chats.models import Chatroom, ChatMessage
from dicts.helpers import get_admin_change_link


@admin.register(Chatroom)
class ChatroomAdmin(admin.ModelAdmin):
    list_select_related = ("trip", "owner")
    list_display = ("pk", "name", "type", "get_trip_link", "get_owner_link")

    def get_trip_link(self, obj):
        return get_admin_change_link(obj.trip)

    def get_owner_link(self, obj):
        return get_admin_change_link(obj.owner)

    def get_tourists_link(self, obj):
        return get_admin_change_link(obj.tourists)

    get_trip_link.short_description = 'Trip'
    get_owner_link.short_description = 'Owner'
    get_tourists_link.short_description = 'Tourists'


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_select_related = ("profile", "chatroom")
    list_display = ("pk", "text", "get_profile_link", "get_chatroom_link")

    def get_profile_link(self, obj):
        return get_admin_change_link(obj.profile)

    def get_chatroom_link(self, obj):
        return get_admin_change_link(obj.chatroom)

    get_profile_link.short_description = 'Profile'
    get_chatroom_link.short_description = 'Chatroom'
