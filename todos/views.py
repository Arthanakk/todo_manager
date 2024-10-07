from django.shortcuts import render, get_object_or_404, redirect
from .models import Project, Todo
import requests
# Create a new project
def create_project(request):
    if request.method == 'POST':
        title = request.POST['title']
        Project.objects.create(title=title)
        return redirect('project_list')
    return render(request, 'create_project.html')

# List all projects
def project_list(request):
    projects = Project.objects.all()
    return render(request, 'project_list.html', {'projects': projects})

# View a project detail with todos
def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    todos = project.todos.all()
    return render(request, 'project_detail.html', {'project': project, 'todos': todos})

# Add a new todo to the project
def add_todo(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        description = request.POST['description']
        Todo.objects.create(project=project, description=description)
    return redirect('project_detail', project_id=project_id)

# Mark todo as complete
def mark_complete(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id)
    todo.is_completed = True
    todo.save()
    return redirect('project_detail', project_id=todo.project.id)


def export_gist(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    todos = project.todos.all()

    completed = [todo for todo in todos if todo.is_completed]
    pending = [todo for todo in todos if not todo.is_completed]

    summary = f"# {project.title}\n\n"
    summary += f"## Summary: {len(completed)} / {len(todos)} completed\n\n"
    summary += "## Pending Todos\n"
    for todo in pending:
        summary += f"- [ ] {todo.description}\n"
    summary += "## Completed Todos\n"
    for todo in completed:
        summary += f"- [x] {todo.description}\n"

    headers = {
        "Authorization": "token YOUR_GITHUB_TOKEN"
    }
    data = {
        "files": {
            f"{project.title}.md": {
                "content": summary
            }
        },
        "public": False
    }
    response = requests.post('', json=data, headers=headers)

    if response.status_code == 201:
        return redirect('project_detail', project_id=project_id)
    else:
        return render(request, 'error.html', {'message': 'Failed to export gist'})

