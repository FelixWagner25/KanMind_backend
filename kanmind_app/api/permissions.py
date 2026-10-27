from rest_framework import permissions
from rest_framework.exceptions import NotFound
from kanmind_app.models import Board, Task


class IsOwnerOrMember(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if obj.members.filter(pk=request.user.pk).exists():
            return True
        return request.user == obj.owner


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner


class IsBoardMemberCreate(permissions.BasePermission):

    def has_permission(self, request, view):
        board_id = request.data.get("board")
        if not Board.objects.filter(id=board_id).exists():
            raise NotFound("Board does not exists.")
        return Board.objects.filter(id=board_id, members=request.user).exists()


class IsBoardMemberDetail(permissions.BasePermission):

    def has_permission(self, request, view):
        task_id = view.kwargs.get("task_id")
        if not Task.objects.filter(id=task_id).exists():
            raise NotFound("Task does not exists.")
        return Task.objects.filter(id=task_id, board__members=request.user).exists()


class IsBoardOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.board.owner == request.user


class IsCreator(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user == obj.creator


class IsAuthor(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user == obj.author
