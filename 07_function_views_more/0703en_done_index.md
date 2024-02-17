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

First we will completely refactor the view, restructurizing it for more convenient procedural dashboard rendering, adding more widget options while reducing code per widget to both define in the view and render:

* creating separate lists for common and user dashboards widgets as tuples, containing widget title as 0th item, data as 1st item, and optionally link to view as 2nd item
* to reduce amount of code we will use intermediate variables for querysets
* pack dashboards and up to 5 `undone_tasks` list to context

```Python
User = get_user_model()

def index(request: HttpRequest) -> HttpResponse:
    tasks = models.Task.objects
    undone_tasks = tasks.filter(is_done=False)
    common_dashboard = [
        (_('users').capitalize(), User.objects.count()),
        (
            _('projects').capitalize(), 
            models.Project.objects.count(), 
            reverse('project_list'),
        ),
        (
            _('tasks').capitalize(), 
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
            _('done tasks').capitalize(), 
            tasks.filter(is_done=True).count(),
        ),
    ]
    if request.user.is_authenticated:
        user_tasks = tasks.filter(owner=request.user)
        user_undone_tasks = user_tasks.filter(is_done=False)
        user_dashboard = [
            (
                _('projects').capitalize(), 
                models.Project.objects.filter(owner=request.user).count(), 
                reverse('project_list') + f"?owner={request.user.username}",
            ),
            (
                _('tasks').capitalize(), 
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
```

as you see, if user is not logged in, we set it's dashboard to empty, and put most recent undone tasks from all users. URL pattern doesn't change, so let's fix up the [index template](../tasker_04/tasks/templates/tasks/index.html) now, which is a complete rewrite. There we just render toolbar widgets in for loops, and we check if the link is defined to render anchor tags. Recent tasks list we just repeat the `for loop` from [task_list template](../tasker_04/tasks/templates/tasks/task_list.html), reducing on done/not done logic since all tasks will be not done.

As you see, we have defined UL's for dashboards with CSS class `dashboard`, so we can style them:

```CSS
ul.dashboard {
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    gap: 1rem;
}

ul.dashboard li {
    display: inline-block;
    border: 2px solid #999999;
    border-radius: 1rem;
}

ul.dashboard li h3 {
    border-radius: 1rem;
    text-align: center;
}

ul.dashboard li .stat {
    display: block;
    text-align: center;
    font-size: 2rem;
    font-weight: 700;
    margin: 1rem;
    padding: 0.5rem;
    background-color: #ffffff9f;
    border-radius: 5rem;
    min-width: 7rem;
}
```

Here we made dashboard lists as horizontal inline block lists with wrapping on - meaning if widgets do not fit into screen's width, they will wrap to the next line instead of creating ugly horizontal scrollbar. In some design choices, that actually would also be an option, but it would be then neater to make it `overflow: scroll-x` and limit it's width to `100vw`; We have also done some rounded design for widgets and some spacing. You are free to experiment with the style here.

## Conclusions

While generic views are best to be implemented as class based views, sometimes niche functionality views like `task_done` or `index`, which do not have fit the generics (list/detail/create/update/delete), are better left as function based views.

## Assignment

Improve the dashboard for your blog. You are free to name it as you wish, probably to represent the generic outlook of the content you promote. Maybe it could be a preview of featured articles with "read more" links... Turn on your imagination, because possibilities are endless here.

Similarly to `task_done` view, you can enable `is_public` state for the page, and modify the page detail view to not render the content if user is not superuser or owner, and even for those authenticated users clearly mark the page as "NOT PUBLISHED".
