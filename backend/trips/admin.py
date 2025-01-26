from django.contrib import admin
from .models import Trip, TripActivity, Ticket, FYQ

@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_select_related = ('creator',)
    list_display = ('creator', 'start_date', 'end_date', 'budget')
    search_fields = ('creator__user__username',)
    list_filter = ('start_date', 'end_date')


@admin.register(TripActivity)
class TripActivityAdmin(admin.ModelAdmin):
    list_select_related = ('trip__creator',)
    list_display = ('name', 'trip', 'budget', 'date')
    search_fields = ('name', 'trip__creator__user__username')
    list_filter = ('date',)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_select_related = ('trip',)
    list_display = ('profile', 'trip', 'activity', 'ticket')
    search_fields = ('profile__user__username', 'trip__creator__user__username', 'activity__name')
    list_filter = ('trip', 'activity')


@admin.register(FYQ)
class FYQAdmin(admin.ModelAdmin):
    list_display = ('id',)
