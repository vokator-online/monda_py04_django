from typing import Any
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.views import generic
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import datetime
from . import models, forms

User = get_user_model()

def index(request: HttpRequest) -> HttpResponse:
    tasks = models.Task.objects
    undone_tasks = tasks.filter(is_done=False)
    common_dashboard = [
        (_('users').title(), User.objects.count()),
        (
            _('projects').title(), 
            models.Project.objects.count(), 
            reverse('project_list'),
        ),
        (
            _('tasks').title(), 
            tasks.count(), 
            reverse('task_list'),
        ),
        (
            _('undone tasks').title(), 
            undone_tasks.count(),
        ),
        (
            _('overdue tasks').title(), 
            undone_tasks.filter(deadline__lte=datetime.now()).count(),
        ),
        (
            _('done tasks').title(), 
            tasks.filter(is_done=True).count(),
        ),
    ]
    if request.user.is_authenticated:
        user_tasks = tasks.filter(owner=request.user)
        user_undone_tasks = user_tasks.filter(is_done=False)
        user_dashboard = [
            (
                _('projects').title(), 
                models.Project.objects.filter(owner=request.user).count(), 
                reverse('project_list') + f"?owner={request.user.username}",
            ),
            (
                _('tasks').title(), 
                user_tasks.count(),
                reverse('task_list') + f"?owner={request.user.username}",
            ),
            (
                _('undone tasks').title(), 
                user_undone_tasks.count(),
            ),
            (
                _('overdue tasks').title(), 
                user_undone_tasks.filter(deadline__lte=datetime.now()).count(),
            ),
        ]
        undone_tasks = user_undone_tasks.all()[:5]
    else:
        user_dashboard = None
        undone_tasks = undone_tasks.all()[:5]
    context = {
        'common_dashboard': common_dashboard,
        'user_dashboard': user_dashboard,
        'undone_tasks': undone_tasks,
    }
    return render(request, 'tasks/index.html', context)

def task_list(request: HttpRequest) -> HttpResponse:
    queryset = models.Task.objects
    owner_username = request.GET.get('owner')
    if owner_username:
        owner = get_object_or_404(User, username=owner_username)
        queryset = queryset.filter(owner=owner)
        projects = models.Project.objects.filter(owner=owner)
    elif request.user.is_authenticated:
        projects = models.Project.objects.filter(owner=request.user)
    else:
        projects = models.Project.objects
    project_pk = request.GET.get('project_pk')
    if project_pk:
        project = get_object_or_404(models.Project, pk=project_pk)
        queryset = queryset.filter(project=project)
    search_name = request.GET.get('search_name')
    if search_name:
        queryset = queryset.filter(name__icontains=search_name)
    next = request.path + '?' + '&'.join([f"{key}={value}" for key, value in request.GET.items()])
    context = {
        'task_list': queryset.all(),
        'project_list': projects.all(),
        'user_list': User.objects.all().order_by('username'),
        'next': next,
    }
    return render(request, 'tasks/task_list.html', context)

def task_detail(request: HttpRequest, pk:int) -> HttpResponse:
    return render(request, 'tasks/task_detail.html', {
        'task': get_object_or_404(models.Task, pk=pk)
    })

@login_required
def task_done(request: HttpRequest, pk:int) -> HttpResponse:
    task = get_object_or_404(models.Task, pk=pk)
    if request.user in [task.owner, task.project.owner]:
        task.is_done = not task.is_done
        task.save()
        messages.success(request, "{} {} {} {}".format(
            _('task').capitalize(),
            task.name,
            _('marked as'),
            _('done') if task.is_done else _('undone'),
        ))
    else:
        messages.error(request, "{}: {}".format(
            _("permission error").title(),
            _("you must be the owner of either the task itelf or it's project"),
        ))
    if request.GET.get('next'):
        return redirect(request.GET.get('next'))
    return redirect(task_list)

@login_required
def task_create(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = forms.TaskForm(request.POST)
        if form.is_valid():
            form.instance.owner = request.user
            form.save()
            messages.success(request, _("task created successfully").capitalize())
            return redirect('task_list')
    else:
        form = forms.TaskForm()
    form.fields['project'].queryset = form.fields['project'].queryset.filter(owner=request.user)
    return render(request, 'tasks/task_create.html', {'form': form})

@login_required
def task_update(request: HttpRequest, pk: int) -> HttpResponse:
    task = get_object_or_404(models.Task, pk=pk, owner=request.user)
    if request.method == "POST":
        form = forms.TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, _("task edited successfully"))
            return redirect('task_detail', pk=pk)
    else:
        form = forms.TaskForm(instance=task)
    form.fields['project'].queryset = form.fields['project'].queryset.filter(owner=request.user)
    return render(request, 'tasks/task_update.html', {'form': form})

@login_required
def task_delete(request: HttpRequest, pk: int) -> HttpResponse:
    task = get_object_or_404(models.Task, pk=pk, owner=request.user)
    if request.method == "POST":
        task.delete()
        messages.success(request, _("task deleted successfully"))
        return redirect('task_list')
    return render(request, 'tasks/task_delete.html', {'task': task})

class ProjectListView(generic.ListView):
    model = models.Project
    template_name = 'tasks/project_list.html'

    def get_queryset(self) -> QuerySet[Any]:
        queryset = super().get_queryset()
        if self.request.GET.get('owner'):
            queryset = queryset.filter(owner__username=self.request.GET.get('owner'))
        return queryset

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['user_list'] = User.objects.all().order_by('username')
        return context


class ProjectDetailView(generic.DetailView):
    model = models.Project
    template_name = 'tasks/project_detail.html'


class ProjectCreateView(LoginRequiredMixin, generic.CreateView):
    model = models.Project
    template_name = 'tasks/project_create.html'
    fields = ('name', 'description', )

    def get_success_url(self) -> str:
        messages.success(self.request, _('project created successfully').capitalize())
        return reverse('project_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProjectUpdateView(
        LoginRequiredMixin, 
        UserPassesTestMixin, 
        generic.UpdateView
    ):
    model = models.Project
    template_name = 'tasks/project_update.html'
    fields = ('name', 'description', )

    def get_success_url(self) -> str:
        messages.success(self.request, _('project updated successfully').capitalize())
        return reverse('project_list')

    def test_func(self) -> bool | None:
        return self.get_object().owner == self.request.user


class ProjectDeleteView(
        LoginRequiredMixin, 
        UserPassesTestMixin, 
        generic.DeleteView
    ):
    model = models.Project
    template_name = 'tasks/project_delete.html'

    def get_success_url(self) -> str:
        messages.success(self.request, _('project deleted successfully').capitalize())
        return reverse('project_list')

    def test_func(self) -> bool | None:
        return self.get_object().owner == self.request.user
