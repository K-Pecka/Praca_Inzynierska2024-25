from django.contrib import admin

from payments.models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'is_paid', 'subscription_type', 'created_at')
    list_filter = ('is_paid', 'subscription_type', 'created_at')
    search_fields = ('user__email', 'stripe_session_id', 'subscription_type')
    ordering = ('-created_at',)