from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import SystemVariable
from .serializers import SystemVariableSerializer

class SystemVariableViewSet(viewsets.ModelViewSet):
    queryset = SystemVariable.objects.all()
    serializer_class = SystemVariableSerializer

    @action(detail=False, methods=['get'], url_path='by-name/(?P<name>[^/.]+)')
    def get_by_name(self, request, name=None):
        var = get_object_or_404(SystemVariable, name=name)
        serializer = self.get_serializer(var)
        return Response(serializer.data)

    @action(detail=False, methods=["list"])
    def get_many(self, request):
        names = request.data.get("names", [])
        if not isinstance(names, list):
            return Response({"error": "'names' must be a list"}, status=400)

        variables = SystemVariable.objects.filter(name__in=names)
        result = {var.name: var.value for var in variables}
        return Response(result)
