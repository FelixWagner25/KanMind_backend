from rest_framework import permissions


class IsOwnerOrMember(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if obj.members.filter(pk=request.user.pk).exists():
            return True
        return request.user == obj.owner


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner


class IsAssignee(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user == obj.assignee
