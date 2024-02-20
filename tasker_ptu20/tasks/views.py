from typing import Any
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views import generic
from . import models


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
        context['user_list'] = get_user_model().objects.all()
        return context


class ProjectDetailView(generic.DetailView):
    model = models.Project
    template_name = 'tasks/project_detail.html'


class ProjectCreateView(LoginRequiredMixin, generic.CreateView):
    model = models.Project
    template_name = 'tasks/project_create.html'
    fields = ('name', )
    
    def get_success_url(self) -> str:
        messages.success(self.request, 
            _('project created succesfully').capitalize())
        return reverse('project_list')
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProjectUpdateView(LoginRequiredMixin,
        UserPassesTestMixin,
        generic.UpdateView,
    ):
    model = models.Project
    template_name = 'tasks/project_update.html'
    fields = ('name', )

    def get_success_url(self) -> str:
        messages.success(self.request, 
            _('project updated succesfully').capitalize())
        return reverse('project_list')

    def test_func(self) -> bool | None:
        return self.get_object().owner == self.request.user or self.request.user.is_superuser


class ProjectDeleteView(LoginRequiredMixin,
        UserPassesTestMixin,
        generic.DeleteView,
    ):
    model = models.Project
    template_name = 'tasks/project_delete.html'

    def get_success_url(self) -> str:
        messages.success(self.request, 
            _('project deleted succesfully').capitalize())
        return reverse('project_list')

    def test_func(self) -> bool | None:
        return self.get_object().owner == self.request.user or self.request.user.is_superuser


def index(request: HttpRequest) -> HttpResponse:
    context = {
        'projects_count': models.Project.objects.count(),
        'tasks_count': models.Task.objects.count(),
        'users_count': models.get_user_model().objects.count(),
    }
    return render(request, 'tasks/index.html', context)

def task_list(request: HttpRequest) -> HttpResponse:
    return render(request, 'tasks/task_list.html', {
        'task_list': models.Task.objects.all(),
    })

def task_detail(request: HttpRequest, pk: int) -> HttpResponse:
    return render(request, 'tasks/task_detail.html', {
        'task': get_object_or_404(models.Task, pk=pk),
    })

def task_done(request: HttpRequest, pk: int) -> HttpResponse:
    task = get_object_or_404(models.Task, pk=pk)
    task.is_done = not task.is_done
    task.save()
    messages.success(request, "{} {} {} {}".format(
        _('task').capitalize(),
        task.name,
        _('marked as'),
        _('done') if task.is_done else _('undone'),
    ))
    if request.GET.get('next'):
        return redirect(request.GET.get('next'))
    return redirect(task_list)
