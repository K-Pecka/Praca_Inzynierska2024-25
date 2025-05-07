from django.contrib import admin
from .models import Trip, Ticket, TicketType, ExpenseType, Expense, TripAccessToken


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_select_related = ('creator',)
    list_display = ('id', 'creator', 'start_date', 'end_date')
    search_fields = ('creator__user__username',)
    list_filter = ('start_date', 'end_date')


@admin.register(TicketType)
class TicketTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    list_filter = ('name',)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_select_related = ('trip', 'owner', 'type')
    list_display = ('id', 'owner', 'trip', 'type', 'valid_from_date', 'valid_from_time')
    search_fields = ('owner__user__email', 'trip__name', 'trip__creator__user__email')
    list_filter = ('trip', 'type')
    filter_horizontal = ('profiles',)


@admin.register(ExpenseType)
class ExpenseTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    list_filter = ('name',)


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_select_related = ('trip', 'user', 'category')
    list_display = ('title', 'amount', 'date', 'note', 'trip', 'user', 'category')
    list_filter = ('trip', 'category', 'date')
    search_fields = ('title', 'note', 'user__user__first_name', 'user__user__last_name')
    date_hierarchy = 'date'


@admin.register(TripAccessToken)
class TripAccessTokenAdmin(admin.ModelAdmin):
    list_select_related = ('trip', 'user_profile')
    list_display = ('trip', 'token', 'user_profile')
    list_filter = ('trip',)
