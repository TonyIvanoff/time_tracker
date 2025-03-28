
from task_tracker.models import Task
from django.shortcuts import render, get_object_or_404, redirect
from datetime import datetime
from django.utils import timezone  # Import timezone utilities
from django.utils.timezone import make_aware


def index(request):
    num_tasks = Task.objects.all().count()
    # Get the sorting field and order from query parameters
    sort_by = request.GET.get('sort_by', 'created_at')  # Default to 'created_at'
    order = request.GET.get('order', 'asc')  # Default to ascending order

    # Determine the sorting order
    if order == 'desc':
        sort_by = f'-{sort_by}'  # Add '-' for descending order

     #Fetch and sort tasks
    tasks = Task.objects.all().order_by(sort_by)

    context = {
        'tasks': tasks,
        'current_sort_by': request.GET.get('sort_by', 'created_at'),
        'current_order': request.GET.get('order', 'asc'),
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
            

        # Update other task fields if needed
        task.type = request.POST.get('type')
        task.status = request.POST.get('status')
        task.save()

        return redirect('task_detail', pk=task.pk)

    comments = task.comments.all()  # Fetch all comments for the task
    return render(request, 'task_tracker/task_detail.html', {'task': task, 'comments': comments})