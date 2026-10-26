from rest_framework import routers
from django.urls import path, include
from .views import BoardViewSet, TaskCreateView, TaskUpdateDestroyView, TaskAssingedToMeView, TaskReviewingView, TaskCommentView, TaskCommentDestroyView, EmailCheckView

router = routers.SimpleRouter()
router.register(r'boards', BoardViewSet)

urlpatterns = [
    path('email-check/', EmailCheckView.as_view()),
    path('tasks/assigned-to-me/', TaskAssingedToMeView.as_view()),
    path('tasks/reviewing/', TaskReviewingView.as_view()),
    path('tasks/', TaskCreateView.as_view()),
    path('tasks/<int:pk>/', TaskUpdateDestroyView.as_view()),
    path('tasks/<int:task_id>/comments/', TaskCommentView.as_view()),
    path('tasks/<int:task_id>/comments/<int:pk>/',
         TaskCommentDestroyView.as_view()),
    path('', include(router.urls)),
]
