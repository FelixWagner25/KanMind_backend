from rest_framework import routers
from django.urls import path, include
from .views import BoardViewSet, TaskViewSet, TaskAssingedToMeViewSet, TaskReviewingViewSet

router = routers.SimpleRouter()
router.register(r'boards', BoardViewSet)
router.register(r'tasks', TaskViewSet)

urlpatterns = [
    path('tasks/assigned-to-me/', TaskAssingedToMeViewSet.as_view()),
    path('tasks/reviewing/', TaskReviewingViewSet.as_view()),
    path('', include(router.urls)),
]
