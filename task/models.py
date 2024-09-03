from django.db import models
from datetime import date, timedelta
import datetime

from goals.models import Goal
from django.utils import timezone

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

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.title)

    def is_completed_today(self):
        return TaskCompletion.objects.filter(task=self, completed_date=date.today()).exists()

    def is_completed_this_week(self):
        # get current time
        now = timezone.now()

        # calculate start of the week (Monday 00:00:00)
        start_of_week = (now - timedelta(days=now.weekday(), hours=now.hour, minutes=now.minute, seconds=now.second,
                                         microseconds=now.microsecond)).date()

        # calculate end of the week (Sunday 23:59:59)
        end_of_week = start_of_week + timedelta(days=6)

        return TaskCompletion.objects.filter(task=self, completed_date__range=[start_of_week, end_of_week]).exists()

    def is_completed(self):
        return TaskCompletion.objects.filter(task=self, completed_date__isnull=False).exists()

class TaskCompletion(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='completions')
    completed_date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return f'Completed {self.task.title} on {self.completed_date}'


