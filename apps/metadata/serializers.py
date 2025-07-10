from rest_framework import serializers
from .models import Metadata


class MetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metadata
        fields = ["name", "value", "created_at"]
        read_only_fields = ["created_at"]
        extra_kwargs = {"name": {"required": True}, "value": {"required": True}}

    def validate_name(self, value):
        """
        Validate that the metadata name doesn't already exist
        """
        if Metadata.objects.filter(name=value).exists():
            raise serializers.ValidationError(
                "A metadata entry with this name already exists."
            )
        return value
