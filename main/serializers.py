from django.utils.html import strip_tags
from rest_framework import serializers

from main.models import Organization


class OrganizationSerializer(serializers.ModelSerializer):
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()

    class Meta:
        model = Organization
        fields = [
            "id", "title", "category", "desc_1", "desc_2", "desc_3",
            "thumbnail", "started_at", "ended_at",
            "star_count", "is_starred", "starred_by_names",
        ]
        read_only_fields = ["id"]

    def validate_title(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Title cannot be empty.")
        return value

    def validate_category(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Organization name cannot be empty.")
        return value

    def validate_desc_1(self, value):
        return strip_tags(value) if value is not None else None

    def validate_desc_2(self, value):
        return strip_tags(value) if value is not None else None

    def validate_desc_3(self, value):
        return strip_tags(value) if value is not None else None

    def validate(self, attrs):
        started_at = attrs.get("started_at", getattr(self.instance, "started_at", None))
        ended_at = attrs.get("ended_at", getattr(self.instance, "ended_at", None))
        if started_at and ended_at and ended_at < started_at:
            raise serializers.ValidationError({
                "ended_at": "End date cannot be before start date.",
            })
        return attrs

    def get_star_count(self, obj):
        return obj.starred_by.count()

    def get_is_starred(self, obj):
        request = self.context.get("request")
        if request is None or not request.user.is_authenticated:
            return False
        return request.user in obj.starred_by.all()

    def get_starred_by_names(self, obj):
        return ", ".join(user.username for user in obj.starred_by.all())
