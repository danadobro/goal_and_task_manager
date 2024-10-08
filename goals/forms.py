from django import forms
from .models import Goal


class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['name', 'description', 'target_date']
        widgets = {'target_date': forms.DateInput(attrs={'type': 'date'})}



