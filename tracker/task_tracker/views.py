
from task_tracker.models import Task
from django.shortcuts import render, get_object_or_404, redirect
from datetime import datetime
from django.utils import timezone  # Import timezone utilities
from django.utils.timezone import make_aware


def index(request):
    # Handle GET request or invalid form submission
    tasks = Task.objects.all().order_by('-created_at')
    context = {
        'tasks': tasks,
        'current_sort_by': request.GET.get('sort_by', 'created_at'),
        'current_order': request.GET.get('order', 'asc'),
    }
    return render(request, 'task_tracker/index.html', context)


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
        task.description = request.POST.get('description')
        task.type = request.POST.get('type')
        task.status = request.POST.get('status')
        task.save()

        return redirect('task_detail', pk=task.pk)

    comments = task.comments.all()  # Fetch all comments for the task
    return render(request, 'task_tracker/task_detail.html', {'task': task, 'comments': comments})



def create_task(request):
        task = None
        if request.method == 'POST':
            # Get form data
            task_id = request.POST.get('task_id')
            description = request.POST.get('description')
            task_type = request.POST.get('type')
            status = request.POST.get('status')

            # Validate required fields
            if task_id and task_type and status:
                # Create a new task
                task = Task.objects.create(
                    task_id=task_id,
                    description=description,
                    type=task_type,
                    status=status
                )
                # Redirect to the task detail page
                return redirect('task_detail', pk=task.pk)
        return render(request, 'task_tracker/create_task.html', {'task': task})