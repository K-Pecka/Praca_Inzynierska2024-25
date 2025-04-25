from rest_framework import serializers
from .models import SystemVariable

class SystemVariableSerializer(serializers.ModelSerializer):
    value = serializers.JSONField()

    class Meta:
        model = SystemVariable
        fields = ["id", "name", "type", "value"]

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["value"] = instance.value
        return rep

    def update(self, instance, validated_data):
        instance.type = validated_data.get("type", instance.type)
        instance.value = validated_data.get("value", instance.value)
        instance.save()
        return instance

    def create(self, validated_data):
        instance = SystemVariable(
            name=validated_data["name"],
            type=validated_data["type"],
        )
        instance.value = validated_data["value"]
        instance.save()
        return instance
