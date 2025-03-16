from django.urls import path
from .views import join_from_link, invite_user

urlpatterns = [
    path('<int:trip_id>/invite/', invite_user, name='trip_invite'),
    path('join/', join_from_link, name='trip_join'),
]
