from django.shortcuts import render, redirect, get_object_or_404
from datetime import date, datetime
from goals import models
from goals import forms
from task import models as task_models
from task.models import Task, TaskCompletion
from goals.forms import GoalForm
from task.forms import TaskForm
from goals.models import Goal
from django.utils import timezone
from datetime import timedelta
from django.db.models import F
from django.views.decorators.http import require_POST
from django.http import JsonResponse


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
    # missed_tasks = Task.objects.filter(goal=goal, completed=False, due_date__lt=datetime.now())
    # completed_tasks = Task.objects.filter(goal=goal, completed=True)
    daily_tasks = Task.objects.filter(goal=goal, type='d')
    weekly_tasks = Task.objects.filter(goal=goal, type='w')
    onetime_tasks = Task.objects.filter(goal=goal, type='one-time')

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
        # 'missed_tasks': missed_tasks,
        # 'completed_tasks': completed_tasks,
        'daily_tasks': daily_tasks,
        'weekly_tasks': weekly_tasks,
        'onetime_tasks': onetime_tasks,
    }
    return render(request, 'goal_detail.html', context)


def mark_task_complete(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        TaskCompletion.objects.create(task=task, completed_date=timezone.now().date())
    goal_id = task.goal.id
    return redirect('goal_detail', pk=goal_id)


def get_completion_dates(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    completion_dates = task.completions.values_list('completed_date', flat=True)
    # Convert datetime objects to string
    completion_dates = [date.strftime('%Y-%m-%d') for date in completion_dates]
    return JsonResponse({'completion_dates': completion_dates})


