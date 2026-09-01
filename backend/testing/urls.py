from django.urls import path
from . import views

urlpatterns = [
    path('', views.test_review, name='test_review'),
    path('<int:topic_id>/', views.test_review_attempts, name='test_review_attempts'),
    path('history/', views.test_history, name='test_history'),
    path('take/', views.take_test_topics, name='take_test_topics'),
    path('take/<int:topic_id>/', views.take_test, name='take_test'),
    path('take/<int:topic_id>/submit/', views.submit_test, name='submit_test'),
    path('result/<int:attempt_id>/', views.test_result, name='test_result'),
]