from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from itineraries.serializers.itinerary_activity_type_serializers import ItineraryActivityTypeListSerializer


@extend_schema(tags=['itinerary activity type'])
class ItineraryActivityTypeListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ItineraryActivityTypeListSerializer

