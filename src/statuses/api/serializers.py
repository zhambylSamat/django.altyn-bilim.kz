from rest_framework import serializers
from ..models import UserStatus


class UserStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserStatus
        fields = (
            'user',
            'description',
            'is_active',
            'created_date'
        )
        read_only_fields = ('user', 'description', 'is_active', 'created_date')
