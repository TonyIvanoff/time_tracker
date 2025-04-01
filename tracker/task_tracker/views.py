from task_tracker.models import Task
from django.shortcuts import render, get_object_or_404, redirect
from datetime import datetime
from django.utils.timezone import make_aware
from django.core.paginator import Paginator


def index(request):
    # Get sorting parameters from request
    sort_by = request.GET.get('sort_by', 'created_at')
    order = request.GET.get('order', 'desc')
    
    # Define allowed sort fields
    allowed_sort_fields = {
        'task_id': 'task_id',
        'created_at': 'created_at',
        'updated_at': 'updated_at',
        'closed_at': 'closed_at',
        'task_duration': 'task_duration',
        'type': 'type',
        'status': 'status'
    }
    
    # Get the sort field, default to created_at if invalid
    sort_field = allowed_sort_fields.get(sort_by, 'created_at')
    
    # Add minus sign for descending order
    if order == 'desc':
        sort_field = f'-{sort_field}'
    
    # Get all tasks ordered by the sort field
    task_list = Task.objects.all().order_by(sort_field)
    
    # Get the page number from the request, default to 1
    page_number = request.GET.get('page', 1)
    
    # Create a paginator object with 9 items per page
    paginator = Paginator(task_list, 9)
    
    # Get the page object
    page_obj = paginator.get_page(page_number)
    
    context = {
        'tasks': page_obj,
        'current_sort_by': sort_by,
        'current_order': order,
    }
    return render(request, 'task_tracker/index.html', context)


from django.shortcuts import render, get_object_or_404, redirect
from .models import Task, Comment

def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    comments = task.comments.all().order_by('-created_at')

    if request.method == 'POST':
        if 'comment' in request.POST:
            # Only allow comments if task is not completed
            if task.status != 'c':
                comment_text = request.POST.get('comment')
                if comment_text:
                    Comment.objects.create(task=task, comment=comment_text)
            return redirect('task_detail', pk=pk)
        elif 'edit_comment' in request.POST:
            # Only allow comment editing if task is not completed
            if task.status != 'c':
                comment_id = request.POST.get('comment_id')
                new_text = request.POST.get('comment_text')
                if comment_id and new_text:
                    comment = Comment.objects.get(id=comment_id)
                    comment.comment = new_text
                    comment.save()
            return redirect('task_detail', pk=pk)
        else:
            # Handle task update
            old_status = task.status
            task.description = request.POST.get('description')
            task.type = request.POST.get('type')
            task.status = request.POST.get('status')
            
            # If status changes to completed, set closed_at
            if task.status == 'c' and old_status != 'c':
                task.closed_at = datetime.now()
            
            task.save()
            return redirect('task_detail', pk=pk)

    return render(request, 'task_tracker/task_detail.html', {'task': task, 'comments': comments})



def create_task(request):
        task = None
        if request.method == 'POST':
            # Get form data
            task_id = request.POST.get('task_id')
            description = request.POST.get('description')
            task_type = request.POST.get('type')

            # Validate required fields
            if task_id and task_type:
                # Create a new task with default status 'w' (Waiting)
                task = Task.objects.create(
                    task_id=task_id,
                    description=description,
                    type=task_type,
                    status='w'  # Set default status to Waiting
                )
                # Redirect to the task detail page
                return redirect('index')
        return render(request, 'task_tracker/create_task.html', {'task': task})