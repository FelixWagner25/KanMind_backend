import datetime
from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import viewsets
from rest_framework import generics
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404
from kanmind_app.models import Board, Task, Comment
from .serializers import BoardSerializer, BoardDetailSerializer, TaskPostSerializer, TaskPatchSerializer, TaskCommentSerializer, EmailCheckSerializer, EmailQuerySerializer
from .permissions import IsOwnerOrMember, IsOwner, IsAssignee


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
    permission_classes = [IsAuthenticated]
    queryset = Board.objects.all()

    def get_queryset(self):
        user = self.request.user
        allowed_boards = Board.objects.filter(
            Q(owner=user) | Q(members=user)).distinct()
        return allowed_boards

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_serializer_class(self):
        if (self.action == "create" or self.action == "list"):
            return BoardSerializer
        else:
            return BoardDetailSerializer

    def get_permissions(self):
        if self.action == "create":
            permission_classes = [IsAuthenticated]
        elif self.action == "destroy":
            permission_classes = [IsOwner]
        else:
            permission_classes = [IsOwnerOrMember]
        return [permission() for permission in permission_classes]


class TaskCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskPostSerializer
    queryset = Task.objects.all()

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class TaskUpdateDestroyView(generics.GenericAPIView, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    permission_classes = [IsAuthenticated]
    queryset = Task.objects.all()
    serializer_class = TaskPatchSerializer

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class TaskAssingedToMeView(generics.ListAPIView):
    """
    A view for viewing and editing instances of tasks that are assigend to one specific user.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = TaskPostSerializer

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(assignee=user)


class TaskReviewingView(generics.ListAPIView):
    """
    A view for viewing and editing instances of tasks that are assigend to one specific user.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = TaskPostSerializer

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(reviewer=user)


class TaskCommentView(generics.ListCreateAPIView):
    """
    A view for viewing and posting and deleting of task comments.
    """
    permission_classes = [IsAuthenticated]
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
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(task_id=self.kwargs['task_id'])
