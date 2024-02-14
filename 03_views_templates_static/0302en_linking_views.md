# List View

So now we know how to do our own custom frontend for our Django application. Let's work with this then, and create a few function based views to list and manage the tasks of our application.

## Objectives

* Create function based views for:
    * List tasks
    * View task in more detail
* Create HTML templates for the list and detail views.

## List View

Reinforcing what we have learned, a simple page view in Django app requires:

* the view function in `views.py`
    * returning the `render()` function 
    * with template and context as arguments
* entry in `urlpatterns` list in `urls.py` with `path()` function containing `url`, `view` and `name` arguments
* the HTML template file placed in `templates/APP_NAME` folder

Let's do that for the view listing tasks:

In `views.py` we just add the view function:

```Python
def task_list(request: HttpRequest) -> HttpResponse:
    return render(request, 'tasks/task_list.html', {
        'task_list': models.Task.objects.all(),
    })
```

Just returning all the `Task` objects as context for the template.

In `urls.py` we add the entry with that `task_list` function, for `tasks/` url, which we conveniently name `task_list` as well:

```Python
urlpatterns = [
    path('', views.index, name='index'),
    path('tasks/', views.task_list, name='task_list'),
]
```

Finally, we create the template looping through `task_list` list objects and printing their `__str__`.

```HTML
{% extends "base.html" %}
{% block title %}{{ block.super }} list{% endblock title %}
{% block content %}
<h1>Tasks</h1>
{% for task in task_list %}
    <p>{{ task }}</p>
{% endfor %}
{% endblock content %}
```

Same as with index, we do not rewrite all HTML boilerplate, it is enough just to extend the base template and only add the context specific to our view.

Then, you can preview the result at [http://127.0.0.1:8000/tasks/](http://127.0.0.1:8000/tasks/).

## Main Menu in `base.html` template

We can create a simple static menu in the `base.html` and add links to both `index` and `task_list` pages.

```HTML
<header>
    <span class="logo">TASKer</span>
    <ul>
        <li><a href="{% url 'index' %}">Dashboard</a></li>
        <li><a href="{% url 'task_list' %}">Tasks</a></li>
    </ul>
</header>
```

It looks a bit raw for now, but we will create some basic styling in not too distant future to improve on that.

## Detail View

Now let's do the view, where we pass a query parameter through the URL, not only the static name. Then, we will use that query parameter, in this case `pk` variable (primary key), which is of `int` type.

In this view we will also use Django's shortcut function `get_object_or_404` which returns 404 page response if object is not found. We need to import it, just append the `import from django.shortcuts` with `get_object_or_404`.

```Python
from django.shortcuts import render, get_object_or_404
```

The `task_detail` view is very similar to the `task_list` one before, however, we add additional argument to the function after request:

```Python
def task_detail(request: HttpRequest, pk:int) -> HttpResponse:
    return render(request, 'tasks/task_detail.html', {
        'task': get_object_or_404(models.Task, pk=pk)
    })
```

And then we pass that argument to object query for our Task model, where we try to query exactly by object's Primary Key. In case it fails, we get 404 error page.

Let's create URL for the `task_detail` page:

```Python
urlpatterns = [
    # ...
    path('task/<int:pk>/', views.task_detail, name='task_detail'),
]
```

As you see, in the 0th argument we have a variable `<int:pk>` defined as a part of URL pattern. That way, any page displaying details of any task, queried by PK, can be accessed via that URL pattern.

One thing still missing is the `tasks/task_detail.html` template:

```HTML
{% extends "base.html" %}
{% block title %}{{ block.super }} | {{ task }}{% endblock title %}
{% block content %}
<h1>{% if task.is_done %}&#x2611;{% else %}&#x2610;{% endif %}
    {{ task.name }}</h1>
<p>{{ task.owner }} / {{ task.project }}</p>
<p>Deadline: {{ task.deadline }}</p>
<p>{{ task.description }}</p>
<p>Created: {{ task.created_at }}, 
    {% if task.created_at != task.updated_at %}
        updated: {{ task.updated_at }}
    {% endif %}
</p>
{% endblock content %}
```

Then, you can preview the result, for example of the task with PK(id) of 1, at [http://127.0.0.1:8000/task/1/](http://127.0.0.1:8000/task/1/). We have even added some simple logic - in case task creation and update time is the same, only show the creation.

Now it is only natural, that we update `tasks/task_list.html` template to link tasks to their detail pages. At the same time, we will display the checkmark status for `is_done` field, and the deadline. We can also refactor the rendering from paragraph to list item.

```HTML
<ul>
{% for task in task_list %}
<li>
    {% if task.is_done %}&#x2611;{% else %}&#x2610;{% endif %}
    <a href="{% url "task_detail" task.pk %}">{{ task.name }}</a>
    <span style="float:right;">{{ task.deadline }}</span>
</li>
{% empty %}
<li>No Tasks Found</li>
{% endfor %}
</ul>
```

So now we have a fully functioning task viewer, where anyone can view any tasks in full detail. Let's try to do some interactivity.

## Assignment

Assuming you are still working on your blog project:

* Create a list of pages view, url, template.
* Create a detail page view, url, template. If you use a slug field, you can add alternative URL pattern to query page by a slug instead of ID. Mind variable type to be `<slug:slug>`, where first word is data type, 2nd is the argument name.
* Link detail pages from list view.
* Create the header section for `base.html` which includes the main navigation menu.
