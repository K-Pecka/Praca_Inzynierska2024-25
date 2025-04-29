from django.contrib import admin

from itineraries.models import ItineraryActivity, ItineraryActivityType


# Register your models here.

@admin.register(ItineraryActivity)
class ItineraryActivityAdmin(admin.ModelAdmin):
    list_display = ('name', 'type')

@admin.register(ItineraryActivityType)
class ItineraryActivityTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
