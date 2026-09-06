from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.utils import timezone
from learning.models import Topic
from .models import Test, Question, Attempt, Answer
from .serializers import TestSerializer, QuestionSerializer, AttemptSerializer, AnswerSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def topic_test_api(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id, user=request.user)
    test = Test.objects.filter(topic=topic).order_by('-created_at').first()

    if not test:
        return Response({'detail': 'No test available for this topic.'}, status=status.HTTP_404_NOT_FOUND)

    questions = test.questions.all()
    data = {
        'test': TestSerializer(test).data,
        'questions': QuestionSerializer(questions, many=True).data,
    }
    return Response(data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_test_api(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id, user=request.user)
    test = Test.objects.filter(topic=topic).order_by('-created_at').first()

    if not test:
        return Response({'detail': 'No test available for this topic.'}, status=status.HTTP_404_NOT_FOUND)

    answers_input = request.data.get('answers', [])
    if not answers_input:
        return Response({'detail': 'No answers submitted.'}, status=status.HTTP_400_BAD_REQUEST)

    attempt = Attempt.objects.create(test=test, user=request.user)
    questions = {q.id: q for q in test.questions.all()}
    correct_count = 0

    for item in answers_input:
        question = questions.get(item.get('question_id'))
        selected = item.get('selected_option')
        if not question or not selected:
            continue

        is_correct = (selected == question.correct_option)
        if is_correct:
            correct_count += 1

        Answer.objects.create(
            attempt=attempt,
            question=question,
            selected_option=selected,
            is_correct=is_correct,
        )

    total_questions = len(questions)
    score = round((correct_count / total_questions) * 100, 1) if total_questions else 0

    attempt.score = score
    attempt.completed_at = timezone.now()
    attempt.save()

    return Response(AttemptSerializer(attempt).data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def attempt_list_api(request):
    attempts = Attempt.objects.filter(user=request.user).order_by('-started_at')
    serializer = AttemptSerializer(attempts, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def topic_attempts_api(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id, user=request.user)
    attempts = Attempt.objects.filter(user=request.user, test__topic=topic).order_by('-started_at')
    serializer = AttemptSerializer(attempts, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def attempt_detail_api(request, pk):
    attempt = get_object_or_404(Attempt, pk=pk, user=request.user)
    answers = attempt.answers.all().select_related('question')

    data = {
        'attempt': AttemptSerializer(attempt).data,
        'answers': [],
    }
    for answer in answers:
        data['answers'].append({
            'question_text': answer.question.question_text,
            'selected_option': answer.selected_option,
            'correct_option': answer.question.correct_option,
            'is_correct': answer.is_correct,
        })

    return Response(data)