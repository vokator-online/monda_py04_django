# Class Based Views

Django has a very nice class based view architecture, designed to quickly prototype more complex use cases, without growing out into monolithic functional views.

We will create the management workflow for both Project and Task objects on the frontend by using generic Django class based views, which we can inherit in our views and develop further. They also integrate very nicely with Forms and other Django utilities and extensions.

## Objectives

Permissioned CRUD workflow for `Project` object, including views, URL patterns and HTML templates.

* Project List with filter by owner
* Project Detail with management links for the owner
* Create a Project
* Update the Project
* Delete the Project

## Project List and Detail Views

We will work with `tasks` app again, not in `user_profile`.

Firstly, let's import the dependencies required to implement our objectives into our views. We need mixins for permission verification from `auth`, and `generic` from `django.views`. We will need reverse to get URLs by their name for certain views as well.

```Python
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpRequest, HttpResponse
from django.views import generic
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from . import models
```

Then we write the view classes themselves. We only need to inherit the specific generic function of the class (either list or detail), and define model and template_name for it. Other parameters are optional and set by default, and the best practice is to use default values if we can.

```Python
class ProjectListView(generic.ListView):
    model = models.Project
    template_name = 'tasks/project_list.html'


class ProjectDetailView(generic.DetailView):
    model = models.Project
    template_name = 'tasks/project_detail.html'
```

Then let's add URL patterns into `urls.py`:

```Python
urlpatterns = [
    # ...
    path('projects/', views.ProjectListView.as_view(), name='project_list'),
    path('project/<int:pk>/', views.ProjectDetailView.as_view(), name='project_detail'),
]
```

Please pay attention, that instead of just leaving project class name as a second argument, we need to call it's method `.as_view()` for class based views.

And finally, simple yet fitting purpose HTML templates:
* [Project List Template](../tasker_04/tasks/templates/tasks/project_list.html)
* [Project Detail Template](../tasker_04/tasks/templates/tasks/project_detail.html)

The only thing left before testing all these out is menu button in the header section of `base.html`:

```HTML
...
<header>
    ...
    <ul class="nav">
        <li><a href="{% url 'index' %}">{% trans "dashboard"|capfirst %}</a></li>
        <li><a href="{% url 'project_list' %}">{% trans "projects"|capfirst %}</a></li>
    ...
```

So we got a quick shot experience of two views implemented in minutes, fully integrated into our application.

## Project Create View

Let's create a view which allows user to create a project. Note that user authentication related mixins must be inherited before generic mixins.

```Python
class ProjectCreateView(LoginRequiredMixin, generic.CreateView):
    model = models.Project
    template_name = 'tasks/project_create.html'
    fields = ('name', )

    def get_success_url(self) -> str:
        messages.success(self.request, _('project created successfully').capitalize())
        return reverse('project_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
```

This view got a few customizations.

Firstly, we have defined which fields from the model will be exposed to the form, which Django will generate for us from our model structure.

Then, once form is valid, django will call `form_valid()` method, where we set the created object's owner to the user which is currently logged in. And by using `reverse` function from `django.urls`, we can return user to project list with success message attached by overriding.

URL pattern:

```Python
urlpatterns = [
    # ...
    path('projects/create/', views.ProjectCreateView.as_view(), name='project_create'),
    # ...
]
```

And the template: [project_create.html](../tasker_04/tasks/templates/tasks/project_create.html)

Now the only thing left to add is a nice "Create New" button into the project list template.

And here it came to mind to style all our buttons to fit the theme:

```CSS
button, .button {
    background-color: #d8d8d8;
    border: 1px solid #666666;
    border-bottom: 2px solid #004488;
    padding: 0.5rem;
    font-size: 120%;
    cursor: pointer;
}

button:hover, .button:hover {
    background-color: #dfdfdf;
    border-bottom: 2px solid #0055cc;
}
```

As usual, styles go to `static/css/style.css`.

## Project Update View

Very similar to create view, but this time we need a few differences than creation view had:

```Python
class ProjectUpdateView(
        LoginRequiredMixin, 
        UserPassesTestMixin, 
        generic.UpdateView
    ):
    model = models.Project
    template_name = 'tasks/project_update.html'
    fields = ('name', )

    def get_success_url(self) -> str:
        messages.success(self.request, _('project updated successfully').capitalize())
        return reverse('project_list')

    def test_func(self) -> bool | None:
        return self.get_object().owner == self.request.user
```

* `form_valid` method does not need overriding since the inherited one is sufficient.
* Currently logged in user must be project's owner, and `UserPassesTestMixin`'s `test_func` can perform that condition checking.

Then, as always, URL pattern (with object's `pk` argument) goes to `urls.py`:

```Python
urlpatterns = [
    # ...
    path('project/<int:pk>/edit/', views.ProjectUpdateView.as_view(), name='project_update'),
]
```

Then [template](../tasker_04/tasks/templates/tasks/project_update.html).

and we place the mighty 'Edit' button to the project's detail page, visible only if project's owner is currently logged in user:

```HTML
...
{% block content %}
<h1>{{ project.name }}</h1>
{% if project.owner == request.user %}
    <p><a class="button" href="{% url "project_update" project.pk %}">{% trans "edit"|capfirst %}</a></p>
{% endif %}
...
{% endblock content %}
```

So now project owners can rename their projects. It is not too difficult to create a possibility for project owners to delete the projects, and all the tasks related to them.

## Project Delete View

This one is very similar to update view, only istead of form to change values of the object, we have a confirmation form, letting the user to review the deletables and change his mind or proceed.

The view:

```Python
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
```

The URL pattern:

```Python
urlpatterns = [
    # ...
    path('project/<int:pk>/delete/', views.ProjectDeleteView.as_view(), name='project_delete'),
]
```

The [template](../tasker_04/tasks/templates/tasks/project_delete.html)

And the button added next to Edit button, of course only for project owners.

```HTML
...
{% if project.owner == request.user %}
<p>
    <a class="button" href="{% url "project_update" project.pk %}">{% trans "edit"|capfirst %}</a>
    <a class="button" href="{% url "project_delete" project.pk %}">{% trans "delete"|capfirst %}</a>
</p>
{% endif %}
...
```

And it is done. Now you know how to create a simple object-level permissioned frontend management workflow for user related objects.

## Filter by user for projects

Let's add the cherry on the top of our CRUD cake. We can make a simple filter for our project list view, to be filter projects by user.

We need to amend the `ProjectListView` with these additional method overrides:

```Python
    def get_queryset(self) -> QuerySet[Any]:
        queryset = super().get_queryset()
        if self.request.GET.get('owner'):
            queryset = queryset.filter(owner__username=self.request.GET.get('owner'))
        return queryset

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['user_list'] = get_user_model().objects.all().order_by('username')
        return context
```

In `get_queryset()` method we verify if the `owner` argument is sent via HTTP's GET method, and if so, we filter our queryset by the username matching the `owner` GET argument.

And we populate context with the list of users in the `get_context_date()` method.

Then we modify the [project list template](../tasker_04/tasks/templates/tasks/project_list.html) to add the filter form next to the "Create New" button. At this point it makes sense to put it together into one inline "toolbar" block divider.

```HTML
{% block content %}
...
<h1>{% trans "projects"|capfirst %}</h1>
<div class="toolbar">
    <a class="button" href="{% url "project_create" %}">{% trans "create new"|title %}</a>
    <form method="get" action="{{ request.path }}">
        <select name="owner" onchange="this.form.submit();">
            <option value="">{% trans "filter by owner"|capfirst %}</option>
            {% for user in user_list %}
                <option value="{{ user.username }}" {% if user.username == request.GET.owner %}selected{% endif %}>{{ user.first_name }} {{ user.last_name }} ({{ user.username }})</option>
            {% endfor %}
        </select>
    </form>
</div>
...
```

That toolbar requires some CSS directives to look neater in the [style.css](../tasker_04/tasks/static/css/style.css):

```CSS
.toolbar {
    margin: 0.5rem;
}

.toolbar form {
    display: inline;
}

.toolbar form select {
    padding: 0.4rem;
}
```

And that's it. We have a simple user filter for our project list.

Next we are going to do the same with `Task` views, but we will intentionally do that as function based views, so that you can see the difference between the two and choose the right approach, since there is never a universal best choice between class based or functional views.

## Assignment

Create a permissioned management workflow for Category (or any other) object of your blog project frontend, which is one-to-many related to Page and User. 
