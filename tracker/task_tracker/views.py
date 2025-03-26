
from task_tracker.models import Task
from django.shortcuts import render, get_object_or_404, redirect
from datetime import datetime
from django.utils import timezone  # Import timezone utilities


def index(request):
    num_tasks = Task.objects.all().count()
    tasks = Task.objects.all()
    
       
    context = {
        'num_tasks' : num_tasks,
        'tasks' : tasks
    }
    
    return render(request, 'task_tracker/index.html', context=context)


def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        # Get the submitted data
        closed_at = request.POST.get('closed_at')
        task.type = request.POST.get('type')
        task.status = request.POST.get('status')
        task.task_comment = request.POST.get('task_comment')

        # Convert closed_at to a timezone-aware datetime object if it's not empty
        if closed_at:
            naive_closed_at = datetime.strptime(closed_at, '%Y-%m-%dT%H:%M')  # Parse as naive datetime
            task.closed_at = timezone.make_aware(naive_closed_at)  # Convert to timezone-aware datetime

        # Save the task
        task.save()
        return redirect('task_detail', pk=task.pk)  # Redirect to the same page after saving
    return render(request, 'task_tracker/task_detail.html', {'task': task})