from django.db import models
from datetime import date, timedelta

from goals.models import Goal

type_choices = (
    ('one-time', 'One-time'),
    ('d', 'Daily'),
    ('w', 'Weekly'),
)


class Task(models.Model):
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, related_name='goals_tasks')
    title = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=type_choices)
    due_date = models.DateField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    completed_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.title)
