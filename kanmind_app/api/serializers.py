from rest_framework import serializers
from django.contrib.auth.models import User
from kanmind_app.models import Board, Task


class UserSerializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "email", "fullname"]

    def get_fullname(self, obj):
        user_full_name = obj.get_full_name()
        if user_full_name == '':
            return obj.username
        return user_full_name


class BoardSerializer(serializers.ModelSerializer):
    member_count = serializers.SerializerMethodField()
    members = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    member_ids = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=True, write_only=True, source='members')
    owner_id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Board
        fields = ["id", "title", "member_count", "member_ids",
                  "members",  "owner_id"]

    def get_member_count(self, obj):
        return obj.members.count()


class TaskSerializer(serializers.ModelSerializer):
    board = serializers.PrimaryKeyRelatedField(queryset=Board.objects.all())
    assignee = UserSerializer(read_only=True, many=True)
    assignee_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=True, write_only=True, source='assignee')
    reviewer = UserSerializer(read_only=True, many=True)
    reviewer_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=True, write_only=True, source='reviewer')
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ["id", "board", "title", "description", "status", "priority",
                  "assignee_id", "assignee", "reviewer_id", "reviewer", "due_date", "comments_count"]

    def get_comments_count(self, obj):
        return obj.comments.count()
