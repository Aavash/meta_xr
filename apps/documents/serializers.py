from rest_framework import serializers
from .models import Document


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ["name", "file", "uploaded_at"]
        read_only_fields = ["uploaded_at"]
        extra_kwargs = {"name": {"required": True}, "file": {"required": True}}

    def validate_name(self, value):
        """
        Validate that the document name doesn't already exist
        """
        if Document.objects.filter(name=value).exists():
            raise serializers.ValidationError(
                "A document with this name already exists."
            )
        return value

    def validate_file(self, value):
        """
        Add any file validation here (size, type, etc.)
        Example: Limit file size to 5MB
        """
        max_size = 5 * 1024 * 1024  # 5MB
        if value.size > max_size:
            raise serializers.ValidationError(
                f"File too large. Size should not exceed {max_size / 1024 / 1024}MB."
            )
        return value
