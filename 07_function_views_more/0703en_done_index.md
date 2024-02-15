# Permissioned Mark Done view and enhanced index dashboard

## Objectives

* fix `task_done` permissions to limit task and related project owners to be able to mark task done
* add to the `index` view more statistical metrics and re-style the dashboard

## Fixing `task_done` to require ownership

We can check that currently logged in user is either owner of the task itself or the project it is related to. Otherwise we will throw out error message instead of success.

```Python
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
```

Unfortunately, filter and search arguments must be pre-compiled into the next variable from the list view itself, then added with `|orlencode` template filter as the `next` GET variable. Changes to `task_list` view:

```Python
def task_list(request: HttpRequest) -> HttpResponse:
    # ...
    next = request.path + '?' + '&'.join([f"{key}={value}" for key, value in request.GET.items()])
    context = {
        # ...
        'next': next,
    }
    return render(request, 'tasks/task_list.html', context)
```

Anchor tag changes in the [template](../tasker_04/tasks/templates/tasks/task_list.html):

```HTML
{% for task in task_list %}
    <li><a href="{% url 'task_done' task.pk %}?next={{ next|urlencode }}">
        ...
```

Now marking done will persist filters.

### Challenge

Find a way to persist list filters while browsing task details editing/deleting them. Suggestion: store filter/search variables in `task_filters` GET variable and toss it across views (including `form action=`) and process in all the views accordingly. Yes, it got that complicated.

## Making index dashboard more powerful and beautiful

