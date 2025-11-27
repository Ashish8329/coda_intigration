from rest_framework import serializers
from scanner.models import Document, Alert


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ["id", "doc_id", "name", "is_published", "created_at", "updated_at"]


class AlertSerializer(serializers.ModelSerializer):
    document = DocumentSerializer(read_only=True)

    class Meta:
        model = Alert
        fields = [
            "id",
            "document",
            "rule",
            "severity",
            "description",
            "created_at",
            "resolved",
        ]
