from rest_framework import serializers
from .models import Topic, Note


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['id', 'name', 'created_at']
        read_only_fields = ['id', 'created_at']


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['id', 'topic', 'content', 'created_at']
        read_only_fields = ['id', 'created_at']