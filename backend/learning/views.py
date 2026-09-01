from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Topic, Note
from testing.models import Attempt


@login_required(login_url='/admin/login/')
def home(request):
    topics = Topic.objects.filter(user=request.user)
    total_notes = Note.objects.filter(user=request.user).count()
    total_tests = Attempt.objects.filter(user=request.user).count()
    recent_notes = Note.objects.filter(user=request.user).order_by('-created_at')[:5]

    scores = Attempt.objects.filter(user=request.user, score__isnull=False).values_list('score', flat=True)
    avg_score = round(sum(scores) / len(scores), 1) if scores else None

    context = {
        'topics': topics,
        'total_topics': topics.count(),
        'total_notes': total_notes,
        'total_tests': total_tests,
        'avg_score': avg_score,
        'recent_notes': recent_notes,
    }
    return render(request, 'learning/home.html', context)


@login_required(login_url='/admin/login/')
def topic_list(request):
    topics = Topic.objects.filter(user=request.user)
    return render(request, 'learning/topic_list.html', {'topics': topics})


@login_required(login_url='/admin/login/')
def topic_add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            Topic.objects.create(user=request.user, name=name)
            return redirect('topic_list')
    return render(request, 'learning/topic_add.html')


@login_required(login_url='/admin/login/')
def topic_detail(request, pk):
    topic = get_object_or_404(Topic, pk=pk, user=request.user)
    notes = topic.notes.all().order_by('-created_at')
    return render(request, 'learning/topic_detail.html', {'topic': topic, 'notes': notes})


@login_required(login_url='/admin/login/')
def note_add(request, pk):
    topic = get_object_or_404(Topic, pk=pk, user=request.user)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Note.objects.create(topic=topic, user=request.user, content=content)
            return redirect('topic_detail', pk=topic.pk)
    return render(request, 'learning/note_add.html', {'topic': topic})


@login_required(login_url='/admin/login/')
def note_edit(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            note.content = content
            note.save()
            return redirect('topic_detail', pk=note.topic.pk)
    return render(request, 'learning/note_edit.html', {'note': note})


@login_required(login_url='/admin/login/')
def note_delete(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    topic_pk = note.topic.pk
    if request.method == 'POST':
        note.delete()
        return redirect('topic_detail', pk=topic_pk)
    return render(request, 'learning/note_confirm_delete.html', {'note': note})