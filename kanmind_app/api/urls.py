from rest_framework import routers
from django.urls import path, include
from .views import BoardViewSet, TaskViewSet, TaskAssingedToMeViewSet, TaskReviewingViewSet, TaskCommentViewSet, TaskCommentDestroyViewSet, EmailCheckView

router = routers.SimpleRouter()
router.register(r'boards', BoardViewSet)
router.register(r'tasks', TaskViewSet)

urlpatterns = [
    path('email-check/', EmailCheckView.as_view()),
    path('tasks/assigned-to-me/', TaskAssingedToMeViewSet.as_view()),
    path('tasks/reviewing/', TaskReviewingViewSet.as_view()),
    path('tasks/<int:pk>/comments/', TaskCommentViewSet.as_view()),
    path('tasks/<int:task_id>/comments/<int:pk>/',
         TaskCommentDestroyViewSet.as_view()),
    path('', include(router.urls)),
]
