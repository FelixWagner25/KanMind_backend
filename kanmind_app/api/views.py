from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from kanmind_app.models import Board, Task
from .serializers import BoardSerializer, TaskSerializer


class BoardViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing board instances.
    """
    permission_classes = [AllowAny]
    serializer_class = BoardSerializer
    queryset = Board.objects.all()


class TaskViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing task instances.
    """
    permission_classes = [AllowAny]
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
