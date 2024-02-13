# Functional permissioned CRUD Views

We have created most important CRUD based workflow for a permissioned object Project last time. Now we will improve our Task views with similar functionality but keep them function based. Later you will have an option to refactor all of them to class based views.

## Objectives

Update these views:
* `task_list` to get filters by user and project, and search function
* add a link to project and owner's management controls to `taks_detail`
* create `task_create` for logged in user
* create `task_update` and `task_delete` for task owner
* fix `task_done` permissions to limit task and related project owners to be able to mark task done
* `index` to get more statistical metrics and re-style the dashboard

## Filters for the Task List view

Let's begin with something simple - adding a few filters and a search by name query to the `task_list` view:

```Python
# ...
def task_list(request: HttpRequest) -> HttpResponse:
    queryset = models.Task.objects
    project_pk = request.GET.get('project_pk')
    if project_pk:
        project = get_object_or_404(models.Project, pk=project_pk)
        queryset = request.filter(project=project)
    owner_username = request.GET.get('owner_username')
    if owner_username:
        owner = get_object_or_404(get_user_model(), username=owner_username)
        queryset = queryset.filter(owner=owner)
    search_name = request.GET.get('search_name')
    if search_name:
        queryset = queryset.filter(name__icontains=search_name)
    context = {
        'task_list': queryset.all(),
        'project_list': models.Project.all(),
        'user_list': get_user_model().objects.all().order_by('username'),
    }
    return render(request, 'tasks/task_list.html', context)
```

The query process is quite simple: we just collect model query parameter from `request.GET`, then verify if object related to that parameter exists, and update the queryset of throw out 404 page. Then we pack the projects and user lists, together with the resulting task list from the queryset, into the `context` which we pass to the returning `render` function.
