from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from kanmind_app.models import Board, Task
from .serializers import BoardSerializer, TaskSerializer


class BoardViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing board instances.
    """
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]
    serializer_class = BoardSerializer
    queryset = Board.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TaskViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing task instances.
    """
    permission_classes = [AllowAny]
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
