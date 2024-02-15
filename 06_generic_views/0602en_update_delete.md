# Generic Update and Delete Views

Previously we have figured out how generic List, Detail and Create views work. Now we will cover Update and Delete functionality.

## Objectives
* Update the Project
* Delete the Project

## Project Update View

Update view is very similar to the create view, but there are quite significant differences:

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

## Filter projects by user

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

Create a permissioned object management (udpate/delete) workflow for `Category` (or any other) model of your blog project frontend, which is one-to-many related to blog Page and User. URL patterns and HTML templates as well.
