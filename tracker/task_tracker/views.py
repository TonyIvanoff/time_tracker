
from task_tracker.models import Task
from django.shortcuts import render, get_object_or_404, redirect
from datetime import datetime
from django.utils import timezone  # Import timezone utilities
from django.utils.timezone import make_aware


def index(request):
    num_tasks = Task.objects.all().count()
    tasks = Task.objects.all()
    
       
    context = {
        'num_tasks' : num_tasks,
        'tasks' : tasks
    }
    
    return render(request, 'task_tracker/index.html', context=context)


from django.shortcuts import render, get_object_or_404, redirect
from .models import Task, Comment

def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        # Save the comment
        comment_text = request.POST.get('comment')
        if comment_text:
            Comment.objects.create(task=task, comment=comment_text)

        closed_at = request.POST.get('closed_at')
        if closed_at:
            naive_closed_at = datetime.strptime(closed_at, '%Y-%m-%dT%H:%M')  # Parse as naive datetime
            task.closed_at = make_aware(naive_closed_at)
            task.save()

        # Update other task fields if needed
        task.type = request.POST.get('type')
        task.status = request.POST.get('status')
        task.task_comment = request.POST.get('task_comment')
        task.save()

        return redirect('task_detail', pk=task.pk)

    comments = task.comment_set.all()  # Fetch all comments for the task
    return render(request, 'task_tracker/task_detail.html', {'task': task, 'comments': comments})