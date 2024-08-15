from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'type', 'due_date']


class UpdateTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['completed']
        widgets = {
            'completed': forms.CheckboxInput(),
        }
