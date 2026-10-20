import datetime
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from kanmind_app.models import Board, Task, Comment
from .serializers import BoardSerializer, TaskPostSerializer, TaskPatchSerializer, TaskCommentSerializer, EmailCheckSerializer


class EmailCheckView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmailCheckSerializer

    def get_queryset(self):
        check_email = self.request.GET.get("email")

        if not check_email:
            return User.objects.none()

        return User.objects.filter(email=check_email)


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


class TaskReviewingViewSet(generics.ListAPIView):
    """
    A viewset for viewing and editing instances of tasks that are assigend to one specific user
    """
    permission_classes = [AllowAny]
    serializer_class = TaskPostSerializer

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(reviewer=user)


class TaskCommentViewSet(generics.ListCreateAPIView):
    """
    A viewset for viewing and posting and deleting of task comments.
    """
    permission_classes = [AllowAny]
    serializer_class = TaskCommentSerializer

    def get_queryset(self):
        task_id = self.kwargs['pk']
        return Comment.objects.filter(task_id=task_id)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user,
                        created_at=datetime.datetime.now(),
                        task_id=self.kwargs['pk'])


class TaskCommentDestroyViewSet(generics.DestroyAPIView):
    """
    A view for deletion of a task comment.
    """
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Comment.objects.filter(task_id=self.kwargs['task_id'])
