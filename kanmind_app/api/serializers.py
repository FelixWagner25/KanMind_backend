from rest_framework import serializers
from django.contrib.auth.models import User
from kanmind_app.models import Comment, Board, Task


class EmailQuerySerializer(serializers.Serializer):
    """Serializes and implicitly validates a user's email."""

    email = serializers.EmailField(required=True)


class UserSerializer(serializers.ModelSerializer):
    """Serializes user with desired API fields."""

    fullname = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'fullname']

    def get_fullname(self, obj):
        """Returns a user's full name."""
        user_full_name = obj.get_full_name()
        if user_full_name == '':
            return obj.username
        return user_full_name


class TaskPostSerializer(serializers.ModelSerializer):
    """Serializes a task for post methods with the desired API fields."""

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
        fields = ['id', 'board', 'title', 'description', 'status', 'priority',
                  'assignee_id', 'assignee', 'reviewer_id', 'reviewer', 'due_date', 'comments_count']

    def get_comments_count(self, obj):
        """Returns nuber of comments assigned to a task."""
        return obj.comments.count()

    def validate(self, data):
        """Validates assignee and reviewer API fields."""
        board = data['board']
        assignee = data.get('assignee', None)
        reviewer = data.get('reviewer', None)
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
    """Serializes a task with the desired API fields for patch methods."""

    assignee = UserSerializer(read_only=True)
    assignee_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True, source='assignee')
    reviewer = UserSerializer(read_only=True)
    reviewer_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True, source='reviewer')

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'priority',
                  'assignee_id', 'assignee', 'reviewer_id', 'reviewer', 'due_date']

    def validate_assignee_id(self, value):
        """Validates the assignee id."""
        if value is None:
            return self.instance.getattr('assignee', None)

        board = self.instance.board
        if not board.members.filter(pk=value.id).exists():
            raise serializers.ValidationError(
                {"assignee_id": "assignee must be board member."})
        return value

    def validate_reviewer_id(self, value):
        """Validates the reviewer id."""
        if value is None:
            return self.instance.getattr('reviewer', None)

        board = self.instance.board
        if not board.members.filter(pk=value.id).exists():
            raise serializers.ValidationError(
                {"reviewer_id": "reviewer must be board member."})
        return value


class TaskCommentSerializer(serializers.ModelSerializer):
    """Serializes comments with the desired API fields."""

    created_at = serializers.DateTimeField(read_only=True)
    author = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'created_at', 'author', 'content']

    def get_author(self, obj):
        return obj.author.get_full_name()


class TaskSerializer(TaskPostSerializer):
    """Serializes a task in with desired fields in a board retrieve view serialization."""

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'priority',
                  'assignee', 'reviewer', 'due_date', 'comments_count']


class BoardSerializer(serializers.ModelSerializer):
    """Serializes a board with the desired API fields."""

    member_count = serializers.SerializerMethodField()
    members = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=True, write_only=True)
    owner_id = serializers.PrimaryKeyRelatedField(read_only=True)
    ticket_count = serializers.SerializerMethodField()
    tasks_to_do_count = serializers.SerializerMethodField()
    tasks_high_prio_count = serializers.SerializerMethodField()

    class Meta:
        model = Board
        fields = ['id', 'title', 'member_count', 'members', 'ticket_count', 'tasks_to_do_count', 'tasks_high_prio_count',
                  'owner_id']

    def get_member_count(self, obj):
        """Returns a board's member count."""
        return obj.members.count()

    def get_ticket_count(self, obj):
        """Returns a board's task count."""
        return obj.tasks.count()

    def get_tasks_to_do_count(self, obj):
        """Returns a board's number of tasks with status "to_do". """
        return obj.tasks.filter(status='to_do').count()

    def get_tasks_high_prio_count(self, obj):
        """Returns a board's number of tasks with high priority."""
        return obj.tasks.filter(priority='high').count()


class BoardRetrieveSerializer(BoardSerializer):
    """Serializes a board with desired API fields for a retrieve operation."""

    members = UserSerializer(read_only=True, many=True)
    tasks = TaskSerializer(read_only=True, many=True)

    class Meta:
        model = Board
        fields = ['id', 'title', 'owner_id', 'members', 'tasks']


class BoardUpdateSerializer(BoardSerializer):
    """Serializes a board with desired API fields for an update operation."""

    owner_data = UserSerializer(source='owner', read_only=True)
    members_data = UserSerializer(source='members', many=True, read_only=True)
    members = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=True, write_only=True)

    class Meta:
        model = Board
        fields = ['id', 'title', 'owner_data', 'members', 'members_data']
