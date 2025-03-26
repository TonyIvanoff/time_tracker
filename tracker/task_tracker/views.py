from django.shortcuts import render
from task_tracker.models import Task
from django.shortcuts import render, get_object_or_404


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
    context = {
        'task' : task
    }
    return render(request, 'task_tracker/task_detail.html', context=context)