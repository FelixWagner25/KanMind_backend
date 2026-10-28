from rest_framework import serializers
from django.contrib.auth.models import User
from kanmind_app.models import Board, Task, Comment


class EmailQuerySerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class EmailCheckSerializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "email", "fullname"]

    def get_fullname(self, obj):
        user_full_name = obj.get_full_name()
        if user_full_name == '':
            return obj.username
        return user_full_name


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


class TaskPostSerializer(serializers.ModelSerializer):
    board = serializers.PrimaryKeyRelatedField(queryset=Board.objects.all())
    assignee = UserSerializer(read_only=True)
    assignee_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True, source='assignee', required=False, allow_null=True)
    reviewer = UserSerializer(read_only=True)
    reviewer_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True, source='reviewer', required=False, allow_null=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ["id", "board", "title", "description", "status", "priority",
                  "assignee_id", "assignee", "reviewer_id", "reviewer", "due_date", "comments_count"]

    def get_comments_count(self, obj):
        return obj.comments.count()

    def validate(self, data):
        board = data["board"]
        assignee = data.get("assignee", None)
        reviewer = data.get("reviewer", None)

        if assignee is not None:
            if not board.members.filter(id=assignee.id).exists():
                raise serializers.ValidationError(
                    {"assignee_id": "assignee must be board member."})
        if reviewer is not None:
            if not board.members.filter(id=reviewer.id).exists():
                raise serializers.ValidationError(
                    {"reviewer_id": "reviewer must be board member."})

        return data


class TaskPatchSerializer(serializers.ModelSerializer):
    assignee = UserSerializer(read_only=True)
    assignee_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True, source='assignee')
    reviewer = UserSerializer(read_only=True)
    reviewer_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True, source='reviewer')

    class Meta:
        model = Task
        fields = ["id", "title", "description", "status", "priority",
                  "assignee_id", "assignee", "reviewer_id", "reviewer", "due_date"]

    def validate_assignee_id(self, value):
        if value is None:
            return self.instance.getattr("assignee", None)

        board = self.instance.board
        if not board.members.filter(pk=value.id).exists():
            raise serializers.ValidationError(
                {"assignee_id": "assignee must be board member."})
        return value

    def validate_reviewer_id(self, value):
        if value is None:
            return self.instance.getattr("reviewer", None)

        board = self.instance.board
        if not board.members.filter(pk=value.id).exists():
            raise serializers.ValidationError(
                {"reviewer_id": "reviewer must be board member."})
        return value


class TaskCommentSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    author = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "created_at", "author", "content"]


class TaskSerializer(TaskPostSerializer):
    class Meta:
        model = Task
        fields = ["id", "title", "description", "status", "priority",
                  "assignee", "reviewer", "due_date", "comments_count"]


class BoardSerializer(serializers.ModelSerializer):
    member_count = serializers.SerializerMethodField()
    member_ids = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=True, write_only=True, source='members')
    owner_id = serializers.PrimaryKeyRelatedField(read_only=True)
    ticket_count = serializers.SerializerMethodField()
    tasks_to_do_count = serializers.SerializerMethodField()
    tasks_high_prio_count = serializers.SerializerMethodField()

    class Meta:
        model = Board
        fields = ["id", "title", "member_count", "member_ids", "ticket_count", "tasks_to_do_count", "tasks_high_prio_count",
                  "owner_id"]

    def get_member_count(self, obj):
        return obj.members.count()

    def get_ticket_count(self, obj):
        return obj.tasks.count()

    def get_tasks_to_do_count(self, obj):
        return obj.tasks.filter(status="to_do").count()

    def get_tasks_high_prio_count(self, obj):
        return obj.tasks.filter(priority="high").count()


class BoardRetrieveSerializer(BoardSerializer):
    members = UserSerializer(read_only=True, many=True)
    tasks = TaskSerializer(read_only=True, many=True)

    class Meta:
        model = Board
        fields = ["id", "title", "owner_id", "members", "tasks"]


class BoardUpdateSerializer(BoardSerializer):
    owner_data = UserSerializer(source="owner", read_only=True)
    members_data = UserSerializer(source="members", many=True, read_only=True)
    members = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=True, write_only=True)

    class Meta:
        model = Board
        fields = ["id", "title", "owner_data", "members", "members_data"]
