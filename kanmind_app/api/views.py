from rest_framework import viewsets
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from kanmind_app.models import Board, Task
from .serializers import BoardSerializer, TaskPostSerializer, TaskPatchSerializer


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
    # ViewSet functions: list, create, retrieve, updated, partial_update, destroy
    permission_classes = [IsAuthenticated]
    queryset = Task.objects.all()

    def get_serializer_class(self):
        if self.action in ["list", "retrieve", "create"]:
            return TaskPostSerializer

        elif self.action in ["update", "partial_update"]:
            return TaskPatchSerializer


class TaskAssingedToMeViewSet(generics.ListAPIView):
    """
    A viewset for viewing and editing instances of tasks that are assigend to one specific user
    """
    permission_classes = [AllowAny]
    serializer_class = TaskPostSerializer

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(assignee=user)
