from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import viewsets
from rest_framework import generics
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404
from kanmind_app.models import Comment, Board, Task
from .serializers import BoardRetrieveSerializer, BoardSerializer,  BoardUpdateSerializer, EmailQuerySerializer, TaskCommentSerializer, TaskPatchSerializer, TaskPostSerializer, UserSerializer
from .permissions import IsAuthor, IsBoardMemberCreate,  IsBoardMemberDetail, IsBoardOwner, IsCreator, IsOwner, IsOwnerOrMember


class EmailCheckView(generics.RetrieveAPIView):
    """Endpoint for email check view."""
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        """Returns user data is queried email is registered or 404 not found otherwise."""
        serializer = EmailQuerySerializer(data=self.request.GET)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        user = get_object_or_404(User, email=email)
        return user


class BoardViewSet(viewsets.ModelViewSet):
    """CRUD endpoints for boards."""
    queryset = Board.objects.all()

    def get_queryset(self):
        """Returns boards the current user is allowed to see."""
        user = self.request.user
        if self.action == 'list':
            return Board.objects.filter(
                Q(owner=user) | Q(members=user)).distinct()

        return Board.objects.all()

    def perform_create(self, serializer):
        """Saves board instance and assigned current user as board owner."""
        serializer.save(owner=self.request.user)

    def get_serializer_class(self):
        """Selects the appropriate serializer depending on the performed action."""
        if (self.action == 'create' or self.action == 'list'):
            return BoardSerializer
        elif (self.action == 'retrieve'):
            return BoardRetrieveSerializer
        elif (self.action == 'update' or self.action == 'partial_update'):
            return BoardUpdateSerializer

    def get_permissions(self):
        """Selects the appropriate permission depending on the performed action."""
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        elif self.action == 'destroy':
            permission_classes = [IsAuthenticated, IsOwner]
        else:
            permission_classes = [IsAuthenticated, IsOwnerOrMember]
        return [permission() for permission in permission_classes]


class TaskCreateView(generics.CreateAPIView):
    """Endpoint to create tasks."""

    permission_classes = [IsAuthenticated, IsBoardMemberCreate]
    serializer_class = TaskPostSerializer
    queryset = Task.objects.all()

    def perform_create(self, serializer):
        """Saves task and assignes user as task creator."""
        serializer.save(creator=self.request.user)


class TaskUpdateDestroyView(generics.GenericAPIView, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    """Endpoints to patch and delete tasks."""

    queryset = Task.objects.all()
    serializer_class = TaskPatchSerializer
    lookup_url_kwarg = 'task_id'

    def patch(self, request, *args, **kwargs):
        """Updates a task object."""
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """Deletes a task object."""
        return self.destroy(request, *args, **kwargs)

    def get_permissions(self):
        """Selects the appripriate perission. Members can updated tasks, only owner can delete task."""
        if self.request.method == 'PATCH':
            permission_classes = [IsAuthenticated, IsBoardMemberDetail]
        elif self.request.method == 'DELETE':
            permission_classes = [
                IsAuthenticated, (IsBoardOwner | IsCreator)]
        return [permission() for permission in permission_classes]


class TaskAssingedToMeView(generics.ListAPIView):
    """Endpoint to list all tasks assigned to the logged in user."""

    permission_classes = [IsAuthenticated]
    serializer_class = TaskPostSerializer

    def get_queryset(self):
        """Selects and returns tasks where the user is assignee."""
        user = self.request.user
        return Task.objects.filter(assignee=user)


class TaskReviewingView(generics.ListAPIView):
    """Endpoint to list all tasks where the logged in user is reviewing."""

    permission_classes = [IsAuthenticated]
    serializer_class = TaskPostSerializer

    def get_queryset(self):
        """Selects and returns tasks where the user is reviewer."""
        user = self.request.user
        return Task.objects.filter(reviewer=user)


class TaskCommentView(generics.ListCreateAPIView):
    """Endpoints to list and create comments."""

    permission_classes = [IsAuthenticated, IsBoardMemberDetail]
    serializer_class = TaskCommentSerializer

    def get_queryset(self):
        """Selects and returns the comments that are assigned to a certain task."""
        task_id = self.kwargs['task_id']
        return Comment.objects.filter(task_id=task_id).order_by('created_at')

    def perform_create(self, serializer):
        """Saves comment and assignes user as author."""
        serializer.save(author=self.request.user,
                        task_id=self.kwargs['task_id'])


class TaskCommentDestroyView(generics.DestroyAPIView):
    """Endpoint to delete comments."""

    permission_classes = [IsAuthenticated, IsAuthor]
    lookup_url_kwarg = 'comment_id'

    def get_queryset(self):
        """Selects and returns comments that are assigned to a certain task."""
        return Comment.objects.filter(task_id=self.kwargs['task_id'])
