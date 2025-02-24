from django.contrib import admin
from .models import Trip, Ticket, FYQ

@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_select_related = ('creator',)
    list_display = ('creator', 'start_date', 'end_date')
    search_fields = ('creator__user__username',)
    list_filter = ('start_date', 'end_date')


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_select_related = ('trip',)
    list_display = ('profile', 'trip', 'ticket')
    search_fields = ('profile__user__username', 'trip__creator__user__username')
    list_filter = ('trip',)


@admin.register(FYQ)
class FYQAdmin(admin.ModelAdmin):
    list_display = ('id',)
