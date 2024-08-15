from django.shortcuts import render, redirect, get_object_or_404
from datetime import date, datetime
from goals import models
from goals import forms
from task import models as task_models
from task.models import Task
from goals.forms import GoalForm
from task.forms import TaskForm, UpdateTaskForm
from goals.models import Goal
from django.utils import timezone
from datetime import timedelta
from django.db.models import F


def home(request):
    goals = models.Goal.objects.all()  # retrieves all Goal objects from the database.
    one_week_from_now = (timezone.now().date() + timedelta(weeks=1))
    upcoming_tasks = Task.objects.filter(due_date__lte=one_week_from_now)
    return render(request, 'home.html', {'goals': goals, 'upcoming_tasks': upcoming_tasks})


def new_goal(request):
    if request.method == 'POST':
        form = forms.GoalForm(request.POST)
        if form.is_valid():
            goal = form.save()
            return redirect('goal_detail', pk=goal.id)
    else:
        form = forms.GoalForm()
    return render(request, 'new_goal.html', {'form': form})


def goal_detail(request, pk):
    goal = get_object_or_404(Goal, pk=pk)
    missed_tasks = Task.objects.filter(goal=goal, completed=False, due_date__lt=datetime.now())
    completed_tasks = Task.objects.filter(goal=goal, completed=True)

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            new_task = form.save(commit=False)

            if new_task.type == 'one-time':
                pass
            else:
                new_task.due_date = goal.target_date

            new_task.goal = goal
            new_task.save()

            print('Task saved:', new_task)

            return redirect('goal_detail', pk=goal.id)
        else:
            print("form errors:", form.errors)

    else:
        form = TaskForm()
    context = {
        'goal': goal,
        'form': form,
        'missed_tasks': missed_tasks,
        'completed_tasks': completed_tasks,
    }
    return render(request, 'goal_detail.html', context)


def update_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        form = UpdateTaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
    return redirect('home')
