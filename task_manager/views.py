from django.shortcuts import render, redirect, get_object_or_404
from goals import models
from goals import forms


def home(request):
    goals = models.Goal.objects.all()  # retrieves all Goal objects from the database.
    return render(request, 'home.html', {'goals': goals})


def new_goal(request):
    if request.method == 'POST':
        form = forms.GoalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirects to home after successfully creating goal
    else:
        form = forms.GoalForm()
    return render(request, 'new_goal.html', {'form': form})


def goal_detail(request, pk):
    goal = get_object_or_404(forms.Goal, pk=pk)
    return render(request, 'goal_detail.html', {'goal': goal})
