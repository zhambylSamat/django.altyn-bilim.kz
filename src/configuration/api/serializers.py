from rest_framework import serializers

from ..models import SubjectQuizConfiguration


class SubjectQuizConfigurationSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubjectQuizConfiguration
        fields = (
            'pk',
            'subject',
            'is_practice',
            'is_theory',
            'created_date',
        )
        read_only_fields = ('pk', 'created_date')
