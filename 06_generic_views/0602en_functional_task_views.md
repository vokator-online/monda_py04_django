# Functional permissioned CRUD Views

We have created most important CRUD based workflow for a permissioned object Project last time. Now we will improve our Task views with similar functionality but keep them function based. Later you will have an option to refactor all of them to class based views.

## Objectives

Update these views:
* `task_list` to get filters by user and project, and search function
* create `task_create` for logged in user
* create `task_update` and `task_delete` for task owner
* add a link to project and owner's management controls to `taks_detail`
* fix `task_done` permissions to limit task and related project owners to be able to mark task done
* `index` to get more statistical metrics and re-style the dashboard

## Filters for the Task List view

Let's begin with something simple - adding a few filters and a search by name query to the `task_list` view:

```Python
def task_list(request: HttpRequest) -> HttpResponse:
    queryset = models.Task.objects
    project_pk = request.GET.get('project_pk')
    if project_pk:
        project = get_object_or_404(models.Project, pk=project_pk)
        queryset = queryset.filter(project=project)
    owner_username = request.GET.get('owner')
    if owner_username:
        owner = get_object_or_404(get_user_model(), username=owner_username)
        queryset = queryset.filter(owner=owner)
    search_name = request.GET.get('search_name')
    if search_name:
        queryset = queryset.filter(name__icontains=search_name)
    context = {
        'task_list': queryset.all(),
        'project_list': models.Project.objects.all(),
        'user_list': get_user_model().objects.all().order_by('username'),
    }
    return render(request, 'tasks/task_list.html', context)
```

The query process is quite simple: we just collect model query parameter from `request.GET`, then verify if object related to that parameter exists, and update the queryset or throw out 404 page depending on the result. Then we pack the projects and user lists, together with the resulting task list from the queryset, into the `context` which we pass to the returning `render` function.

Now let's fix up the template and add the toolbar with filter controls and search box:

```HTML
...
{% block content %}
<h1>{% trans "tasks"|capfirst %}</h1>
<div class="toolbar">
    {% comment %} <a class="button" href="{% url "project_create" %}">{% trans "create new"|title %}</a> {% endcomment %}
    <form method="get" action="{{ request.path }}">
        <select name="owner" onchange="this.form.submit();">
            <option value="">{% trans "filter by owner"|capfirst %}</option>
            {% for user in user_list %}
                <option value="{{ user.username }}" {% if user.username == request.GET.owner %}selected{% endif %}>{{ user.first_name }} {{ user.last_name }} ({{ user.username }})</option>
            {% endfor %}
        </select>
        <select name="project_pk" onchange="this.form.submit();">
            <option value="">{% trans "filter by project"|capfirst %}</option>
            {% for project in project_list %}
                <option value="{{ project.pk }}" {% if project.pk|slugify == request.GET.project_pk %}selected{% endif %}>{{ project.name }}</option>
            {% endfor %}
        </select>
        <input type="text" name="search_name" value="{{ request.GET.search_name }}" placeholder="search by name...">
        <button type="submit">&#128269;</button>
    </form>
</div>
...
```

We have added two select boxes, prepopulated by contents from `user_list` and `project_list` context items. And we add `search_name` input box either with placeholder explaining it's use or pre-fill from previous query. Also, string and numeric variables ever need to be compared, you can convert integers or floats to string with `|slugify` tag filter.

And it seems that our CSS style needs some amendments:

```CSS
.toolbar form select, .toolbar form input {
    padding: 0.4rem;
}
```

## Create a Task view

Django's generic views generate model forms themselves. With function based views, we either need to create the form ourselves, or render and process it manually. Since Django model forms do a lot of validation, it is a great development effort shortcut and we should use them wherever possible. So let's create a form for `Task` model. For that we will need to create `forms.py` file in our project:

```Python
from django import forms
from . import models


class TaskForm(forms.ModelForm):
    class Meta:
        model = models.Task
        fields = ('name', 'project', 'description', 'deadline', 'is_done' )
```

We need to define `model` and `fields` attributes in `Meta` class of the form class. The model we import from our app models, and fields we define as a tuple of strings with field names. Other arguments are optional and we will cover them much later in the course.

We will need to import `login_required` decorator to views, as well as our form:

```Python
# ...
from django.contrib.auth.decorators import login_required
# ...
from . import models, forms
# ...
```

Then we write the view itself:

```Python
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
        form = forms.TaskForm
    return render(request, 'tasks/task_create.html', {'form': form})
```

This approach is very similar to our user signup view. First we render the empty form, then we try to catch it filled in. If form validates, we assign currently logged in user to the owner of the `Task` object to be created, and save form. Then we let user know of the success and redirect to task list.

As always, the view is accompanied with URL pattern in `urls.py`:

```Python
# ...
urlpatterns = [
    path('', views.index, name='index'),
    path('tasks/', views.task_list, name='task_list'),
    path('tasks/create/', views.task_create, name='task_create'),
    path('task/<int:pk>/', views.task_detail, name='task_detail'),
    path('task/<int:pk>/done/', views.task_done, name='task_done'),
    # ...
```

The [template](../tasker_04/tasks/templates/tasks/task_create.html) is becoming very generic, only wording is different from [Project's create template](../tasker_04/tasks/templates/tasks/project_create.html). In fact, if we would replace the view with class based view, this template would not need a single change to be made to function.

Let's add the button to the toolbar into [task_list.html](../tasker_04/tasks/templates/tasks/task_list.html):

```HTML
...
<h1>{% trans "tasks"|capfirst %}</h1>
<div class="toolbar">
    <a class="button" href="{% url "task_create" %}">{% trans "create new"|title %}</a>
...
```

Now we can test the form. It functions, but kind of asks for a few improvements. Firstly, in project list we want to see only our projects. We can fix that easily in the view itself:

```Python
def task_create(request: HttpRequest) -> HttpResponse:
    # ...
    form.fields['project'].queryset = form.fields['project'].queryset.filter(owner=request.user)
    return render(request, 'tasks/task_create.html', {'form': form})
```

And it would be very nice to have a date picker. We can fix that by overriding `DateTime` widget in [forms.py](../tasker_04/tasks/forms.py) and using it in the form.

