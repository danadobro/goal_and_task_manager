from django.db import models


class Goal(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    target_date = models.DateField()

    def __str__(self):
        return str(self.name)

    def calculate_progress(self):
        total_tasks = self.tasks.count()
        if total_tasks == 0:
            return 0
        completed_tasks = self.tasks.filter(completed=True).count()
        return (completed_tasks / total_tasks) * 100


class Task(models.Model):
    TASK_TYPE_CHOICES = [
        ('weekly', 'Weekly'),
        ('daily', 'Daily'),
        ('one-time', 'One-time'),
    ]
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    task_type = models.CharField(max_length=50, choices=TASK_TYPE_CHOICES)
    completed = models.BooleanField(default=False)
    due_date = models.DateField()

    def __str__(self):
        return self.title


class Progress(models.Model):
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, related_name='progress')
    date = models.DateField(auto_now_add=True)
    percentage_completed = models.FloatField()

    def __str__(self):
        return f"{self.goal.name} - {self.percentage_completed}%"

    def save(self, *args, **kwargs):
        self.percentage_completed = self.goal.calculate_progress()
        super().save(*args, **kwargs)

# Create your models here.
