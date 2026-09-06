from rest_framework import serializers
from .models import Test, Question, Attempt, Answer


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ['id', 'topic', 'title', 'created_at']
        read_only_fields = ['id', 'created_at']


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'question_text', 'option_a', 'option_b', 'option_c', 'option_d']
        read_only_fields = fields


class AttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attempt
        fields = ['id', 'test', 'score', 'started_at', 'completed_at']
        read_only_fields = ['id', 'score', 'started_at', 'completed_at']


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'attempt', 'question', 'selected_option', 'is_correct']
        read_only_fields = ['id', 'is_correct']