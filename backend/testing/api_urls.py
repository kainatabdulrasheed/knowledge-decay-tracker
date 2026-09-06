from django.urls import path
from . import api_views

urlpatterns = [
    path('topics/<int:topic_id>/test/', api_views.topic_test_api, name='api_topic_test'),
    path('topics/<int:topic_id>/test/submit/', api_views.submit_test_api, name='api_submit_test'),
    path('attempts/', api_views.attempt_list_api, name='api_attempt_list'),
    path('topics/<int:topic_id>/attempts/', api_views.topic_attempts_api, name='api_topic_attempts'),
    path('attempts/<int:pk>/', api_views.attempt_detail_api, name='api_attempt_detail'),
]