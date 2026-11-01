from rest_framework import permissions
from rest_framework.exceptions import NotFound
from kanmind_app.models import Board, Task


class IsOwnerOrMember(permissions.BasePermission):
    """Allows access to board owner and board member."""

    def has_object_permission(self, request, view, obj):
        if obj.members.filter(pk=request.user.pk).exists():
            return True
        return request.user == obj.owner


class IsOwner(permissions.BasePermission):
    """Allows access to object's owner."""

    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner


class IsBoardMemberCreate(permissions.BasePermission):
    """Allows access for board members for create operations."""

    def has_permission(self, request, view):
        board_id = request.data.get("board")
        if not Board.objects.filter(id=board_id).exists():
            raise NotFound("Board does not exists.")
        return Board.objects.filter(id=board_id, members=request.user).exists()


class IsBoardMemberDetail(permissions.BasePermission):
    """Allows access for board members for retrieve, update and destroy operations."""

    def has_permission(self, request, view):
        task_id = view.kwargs.get("task_id")
        if not Task.objects.filter(id=task_id).exists():
            raise NotFound("Task does not exists.")
        return Task.objects.filter(id=task_id, board__members=request.user).exists()


class IsBoardOwner(permissions.BasePermission):
    """Allows access for board owner of a specific task."""

    def has_object_permission(self, request, view, obj):
        return obj.board.owner == request.user


class IsCreator(permissions.BasePermission):
    """Allows access for the creator of a task."""

    def has_object_permission(self, request, view, obj):
        return request.user == obj.creator


class IsAuthor(permissions.BasePermission):
    """Allows access for the author of a comment."""

    def has_object_permission(self, request, view, obj):
        return request.user == obj.author
