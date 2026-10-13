from rest_framework import serializers
from kanmind_app.models import Board, Task


class BoardSerializer(serializers.ModelSerializer):
    member_count = serializers.SerializerMethodField()
    owner_id = serializers.PrimaryKeyRelatedField(
        queryset=Board.objects.all(), write_only=True)

    class Meta:
        model = Board
        fields = ["id", "title", "member_count", "members", "owner_id", ]

    def get_member_count(self, obj):
        return obj.members.count()


class TaskSerializer(serializers.ModelSerializer):
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ["id", "board", "title", "description",
                  "assignee", "reviewer", "due_date", "comments_count"]

    def get_comments_count(self, obj):
        return obj.comments.count()
