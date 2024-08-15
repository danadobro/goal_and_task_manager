from django.db import models


class Goal(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    target_date = models.DateField()

    def __str__(self):
        return str(self.name)








