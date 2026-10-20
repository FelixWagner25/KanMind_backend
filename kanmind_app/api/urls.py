from rest_framework import routers
from django.urls import path, include
from .views import BoardViewSet, TaskViewSet, TaskAssingedToMeView, TaskReviewingView, TaskCommentView, TaskCommentDestroyView, EmailCheckView

router = routers.SimpleRouter()
router.register(r'boards', BoardViewSet)
router.register(r'tasks', TaskViewSet)

urlpatterns = [
    path('email-check/', EmailCheckView.as_view()),
    path('tasks/assigned-to-me/', TaskAssingedToMeView.as_view()),
    path('tasks/reviewing/', TaskReviewingView.as_view()),
    path('tasks/<int:pk>/comments/', TaskCommentView.as_view()),
    path('tasks/<int:task_id>/comments/<int:pk>/',
         TaskCommentDestroyView.as_view()),
    path('', include(router.urls)),
]
