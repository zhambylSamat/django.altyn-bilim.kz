from rest_framework import serializers
from ..models import Subject, Topic, Video


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = (
            'pk',
            'title'
        )
        read_only_fields = ('pk',)


class RecursiveTopicField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class ChapterAndTopicSerializer(serializers.ModelSerializer):
    topics = RecursiveTopicField(many=True, required=False)
    selected = serializers.BooleanField(default=True)
    videos = serializers.SerializerMethodField()

    @staticmethod
    def get_videos(topic):
        try:
            videos = topic.t_video.all()
            result = []
            for video in videos:
                result.append({
                    'duration': video.duration
                })
            return result
        except AttributeError:
            return None

    class Meta:
        model = Topic
        fields = (
            'pk',
            'subject',
            'parent',
            'title',
            'is_endpoint',
            'is_mid_control',
            'order',
            'topics',
            'selected',
            'videos'
        )
        read_only_fields = ('pk', 'subject', 'parent', 'title', 'is_endpoint', 'is_mid_control', 'order', 'topics')


class TopicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Topic
        fields = (
            'pk',
            'subject',
            'parent',
            'title',
            'order'
        )


class FullSubjectSerializer(serializers.ModelSerializer):
    topics = serializers.SerializerMethodField(read_only=True)

    @staticmethod
    def get_topics(instance):
        try:
            topics = instance.topic.all().order_by('order')
            return ChapterAndTopicSerializer(topics, many=True).data
        except AttributeError:
            return None

    class Meta:
        model = Subject
        fields = (
            'pk',
            'title',
            'topics',
        )
        read_only_fields = ('pk', )


class VideoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Video
        fields = (
            'pk',
            'topic',
            'title',
            'duration',
            'link',
            'created_date',
        )
