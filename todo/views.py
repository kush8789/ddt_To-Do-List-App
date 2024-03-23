from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from todo.forms import TaskForm
from todo.models import Task

def index(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = TaskForm(data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("index"))

    form = TaskForm()
    tasks = Task.objects.all().order_by("-created")

    context = {
        "tasks": tasks,
        "form": form,
        "Status": Task.StatusChoice,
        "filter_choice": "ALL",
    }

    return render(request, "index.html", context)

def update_task_status(request: HttpRequest, task_id: int, new_status: str) -> HttpResponse:
    task = get_object_or_404(Task, id=task_id)

    if new_status in Task.StatusChoice.values:
        task.status = new_status
        task.save()

    return HttpResponseRedirect(reverse("index"))

def delete_task(request: HttpRequest, task_id: int) -> HttpResponse:
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    
    return HttpResponseRedirect(reverse("index"))

def filter_tasks(request: HttpRequest, status: str) -> HttpResponse:
    if status not in Task.StatusChoice.values:
        return HttpResponseBadRequest("Invalid status")

    if request.method == "POST":
        form = TaskForm(data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("filter", args=[status]))

    tasks = Task.objects.filter(status=status).order_by("-created")
    form = TaskForm()

    context = {
        "tasks": tasks,
        "form": form,
        "Status": Task.StatusChoice,
        "filter_choice": status,
    }

    return render(request, "index.html", context)
