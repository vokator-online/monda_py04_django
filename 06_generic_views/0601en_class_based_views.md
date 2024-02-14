# Class Based Views

Django has a very nice class based view architecture, designed to quickly prototype more complex use cases, without growing out into monolithic functional views.

We will create the management workflow for both Project and Task objects on the frontend by using generic Django class based views, which we can inherit in our views and develop further. They also integrate very nicely with Forms and other Django utilities and extensions.

## Objectives

Permissioned CRUD workflow for `Project` object, including views, URL patterns and HTML templates.

* Project List with filter by owner
* Project Detail with management links for the owner
* Create a Project

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

## Conclusion

Class based generic views have a very clear structure, propagates clean code and simplicity. They can be customized as well as function based views, with the advantage of distributing logic across class methods and avoiding monolithic spaghetti code.

In the next part we will cover generic class based update and deleve views.
