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
    # status = Use TextChoices for this
    # priority = Use TextChoices for this
    assignee = models.ManyToManyField(User, related_name="assignments")
    reviewer = models.ManyToManyField(User, related_name="reviews")
    due_date = models.DateField()


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments")
    created_at = models.DateTimeField()
    content = models.TextField()
