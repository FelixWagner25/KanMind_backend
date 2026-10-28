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
    description = models.TextField(blank=True)
    board = models.ForeignKey(
        Board, on_delete=models.CASCADE, related_name="tasks")
    assignee = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="assignee", null=True, blank=True)
    reviewer = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="reviewer", null=True, blank=True)
    due_date = models.DateField()
    creator = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="creator", null=True, blank=True)

    class Status(models.TextChoices):
        TO_DO = "to_do"
        IN_PROGRESS = "in_progress"
        REVIEW = "review"
        DONE = "done"

    class Priority(models.TextChoices):
        LOW = "low"
        MEDIUM = "medium"
        HIGH = "high"

    status = models.CharField(
        max_length=11, choices=Status.choices, default=Status.TO_DO)
    priority = models.CharField(
        max_length=6, choices=Priority.choices, default=Priority.MEDIUM)

    def __str__(self):
        return f"{self.title} {self.board}"


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments")
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    task = models.ForeignKey(
        "Task", on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return f"{self.author} {self.created_at}" + f"{self.content}"[:10]
