from django.shortcuts import render
from task_tracker.models import Task



def index(request):
    num_tasks = Task.objects.all().count()
    tasks = Task.objects.all()
    
       
    context = {
        'num_tasks' : num_tasks,
        'tasks' : tasks
    }
    
    return render(request, 'tracker/index.html', context=context)


def task_detail(request, task_id):
    task = Task.objects.get(task_id=task_id)
    context = {
        'task' : task
    }
    return render(request, 'tracker/task_detail.html', context=context)