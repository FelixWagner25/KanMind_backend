import datetime
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import get_object_or_404
from kanmind_app.models import Board, Task, Comment
from .serializers import BoardSerializer, TaskPostSerializer, TaskPatchSerializer, TaskCommentSerializer, EmailCheckSerializer, EmailQuerySerializer


class EmailCheckView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmailCheckSerializer

    def get_object(self):
        serializer = EmailQuerySerializer(data=self.request.GET)

        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        user = get_object_or_404(User, email=email)
        return user


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


class TaskAssingedToMeView(generics.ListAPIView):
    """
    A view for viewing and editing instances of tasks that are assigend to one specific user.
    """
    permission_classes = [AllowAny]
    serializer_class = TaskPostSerializer

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(assignee=user)


class TaskReviewingView(generics.ListAPIView):
    """
    A view for viewing and editing instances of tasks that are assigend to one specific user.
    """
    permission_classes = [AllowAny]
    serializer_class = TaskPostSerializer

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(reviewer=user)


class TaskCommentView(generics.ListCreateAPIView):
    """
    A view for viewing and posting and deleting of task comments.
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


class TaskCommentDestroyView(generics.DestroyAPIView):
    """
    A view for deletion of a task comment.
    """
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Comment.objects.filter(task_id=self.kwargs['task_id'])
