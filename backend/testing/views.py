from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from learning.models import Topic
from .models import Test, Question, Attempt, Answer


@login_required(login_url='/admin/login/')
def test_review(request):
    topics = Topic.objects.filter(user=request.user)
    return render(request, 'testing/test_review.html', {'topics': topics})


@login_required(login_url='/admin/login/')
def test_review_attempts(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id, user=request.user)
    attempts = Attempt.objects.filter(user=request.user, test__topic=topic).order_by('-started_at')
    return render(request, 'testing/test_review_attempts.html', {'topic': topic, 'attempts': attempts})


@login_required(login_url='/admin/login/')
def test_history(request):
    attempts = Attempt.objects.filter(user=request.user).order_by('-started_at')
    return render(request, 'testing/test_history.html', {'attempts': attempts})


@login_required(login_url='/admin/login/')
def take_test_topics(request):
    topics = Topic.objects.filter(user=request.user)
    return render(request, 'testing/take_test_topics.html', {'topics': topics})


@login_required(login_url='/admin/login/')
def take_test(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id, user=request.user)
    test = Test.objects.filter(topic=topic).order_by('-created_at').first()

    if not test:
        return render(request, 'testing/no_test_available.html', {'topic': topic})

    questions = test.questions.all()
    return render(request, 'testing/take_test.html', {'topic': topic, 'test': test, 'questions': questions})


@login_required(login_url='/admin/login/')
def submit_test(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id, user=request.user)
    test = Test.objects.filter(topic=topic).order_by('-created_at').first()

    if request.method != 'POST' or not test:
        return redirect('take_test', topic_id=topic.pk)

    attempt = Attempt.objects.create(test=test, user=request.user)
    questions = test.questions.all()
    correct_count = 0

    for question in questions:
        selected = request.POST.get(f'question_{question.id}')
        if not selected:
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

    total_questions = questions.count()
    score = round((correct_count / total_questions) * 100, 1) if total_questions else 0

    attempt.score = score
    attempt.completed_at = timezone.now()
    attempt.save()

    return redirect('test_result', attempt_id=attempt.pk)


@login_required(login_url='/admin/login/')
def test_result(request, attempt_id):
    attempt = get_object_or_404(Attempt, pk=attempt_id, user=request.user)
    answers = attempt.answers.all().select_related('question')
    return render(request, 'testing/test_result.html', {'attempt': attempt, 'answers': answers})