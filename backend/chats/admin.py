from django.contrib import admin

from chats.models import Chatroom, Message
from dicts.helpers import get_admin_change_link


@admin.register(Chatroom)
class ChatroomAdmin(admin.ModelAdmin):
    list_select_related = ("trip", "creator")
    list_display = ("pk", "name", "type", "get_trip_link", "get_creator_link")

    def get_trip_link(self, obj):
        return get_admin_change_link(obj.trip)

    def get_creator_link(self, obj):
        return get_admin_change_link(obj.creator)

    def get_members_link(self, obj):
        return get_admin_change_link(obj.members)

    get_trip_link.short_description = 'Trip'
    get_creator_link.short_description = 'Creator'
    get_members_link.short_description = 'Members'


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_select_related = ("profile", "chatroom")
    list_display = ("pk", "content", "get_profile_link", "get_chatroom_link")

    def get_profile_link(self, obj):
        return get_admin_change_link(obj.profile)

    def get_chatroom_link(self, obj):
        return get_admin_change_link(obj.chatroom)

    get_profile_link.short_description = 'Profile'
    get_chatroom_link.short_description = 'Chatroom'
