from django.urls import path
from . import api_views

urlpatterns = [
    path('topics/', api_views.topic_list_api, name='api_topic_list'),
    path('topics/<int:topic_id>/notes/', api_views.note_list_api, name='api_note_list'),
    path('notes/<int:pk>/', api_views.note_detail_api, name='api_note_detail'),
]