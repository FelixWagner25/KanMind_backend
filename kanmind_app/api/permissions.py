from rest_framework import permissions
from kanmind_app.models import Board


class IsOwnerOrMember(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if obj.members.filter(pk=request.user.pk).exists():
            return True
        return request.user == obj.owner


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner


class IsBoardMember(permissions.BasePermission):

    def has_permission(self, request, view):
        board_id = request.data.get("board")
        if not board_id:
            return False
        return Board.objects.filter(id=board_id, members=request.user).exists()


class IsBoardOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.board.owner == request.user


class IsCreator(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user == obj.creator
