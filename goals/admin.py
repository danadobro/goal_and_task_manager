from django.contrib import admin
from .models import Goal, Task, Progress

admin.site.register(Goal)
admin.site.register(Task)
admin.site.register(Progress)

# Register your models here.
