from django.contrib import admin
from .models import Board, Comment, Task


class BoardAdmin(admin.ModelAdmin):
    list_display = ["title", "owner"]
    list_filter = ["members"]


class TaskAdmin(admin.ModelAdmin):
    list_display = ["title", "board", "description", "creator"]
    list_filter = ["board", "creator", "due_date", "priority", "status"]


class CommentAdmin(admin.ModelAdmin):
    list_display = ["author", "content", "task", "created_at"]
    list_filter = ["author", "created_at", "task"]


admin.site.register(Board, BoardAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Comment, CommentAdmin)
