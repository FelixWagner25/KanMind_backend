from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Board(models.Model):
    title = models.CharField(max_length=255)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="board_ownings")
    members = models.ManyToManyField(User, related_name="boards")

    def __str__(self):
        return f"{self.title}"


class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    board = models.ForeignKey(
        Board, on_delete=models.CASCADE, related_name="tasks")
    assignee = models.ManyToManyField(User, related_name="assignments")
    reviewer = models.ManyToManyField(User, related_name="reviews")
    due_date = models.DateField()

    class Status(models.TextChoices):
        TO_DO = "to_do"
        IN_PROGRESS = "in_progress"
        REVIEW = "review"
        DONE = "done"

    class Priority(models.TextChoices):
        LOW = "low"
        MEDIUM = "medium"
        HIGH = "high"

    def __str__(self):
        return f"{self.title} {self.board}"


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments")
    created_at = models.DateTimeField()
    content = models.TextField()

    def __str__(self):
        return f"{self.author} {self.created_at}" + f"{self.content}"[:10]
