from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Topic, Note
from .serializers import TopicSerializer, NoteSerializer


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def topic_list_api(request):
    if request.method == 'GET':
        topics = Topic.objects.filter(user=request.user)
        serializer = TopicSerializer(topics, many=True)
        return Response(serializer.data)

    serializer = TopicSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def note_list_api(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id, user=request.user)

    if request.method == 'GET':
        notes = topic.notes.all().order_by('-created_at')
        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data)

    serializer = NoteSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user, topic=topic)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def note_detail_api(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)

    if request.method == 'DELETE':
        note.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    partial = request.method == 'PATCH'
    serializer = NoteSerializer(note, data=request.data, partial=partial)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)