# Function based Update and Delete views for Task object

## Objectives

* create `task_update` and `task_delete` for task owner
* add a link to project and owner's management controls to `taks_detail`

## Update (edit) Task view

We will reuse the same form and the view is quite similar. The difference is that we pass a keyword argument `pk` to the view, which helps to query for the object to be edited. We also pass the object to the form's instance. Processing is exactly the same:

```Python
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
```

URL pattern:

```Python
    path('task/<int:pk>/edit/', views.task_update, name='task_update'),
```

Then the [task_update.html](../tasker_04/tasks/templates/tasks/task_update.html) template which is so painfully similar to [project_update.html](../tasker_04/tasks/templates/tasks/project_update.html) template. And this template is also interchangable for the class based view.

Last thing - adding the mighty `Edit` button to the `task_detail.html`:

```HTML
{% if task.owner == request.user %}
    <p>
        <a class="button" href="{% url "task_update" task.pk %}">{% trans "edit"|capfirst %}</a>
        {% comment %} <a class="button" href="{% url "task_delete" task.pk %}">{% trans "delete"|capfirst %}</a> {% endcomment %}
    </p>
{% endif %}
```

The delete button follows the same logic, so we place it there as we will need it very very soon, just we comment it out if we want to test edit functionality first, which we can do now.

## Deleting Task view

While we can implement task deletion in a similar way it is currently with `task_done` view, we should follow the good practice and require user confirmation via POST form. That way we impose some challenge for user interactions have impact and cannot be undone. However the form is empty in this case.

```Python
@login_required
def task_delete(request: HttpRequest, pk: int) -> HttpResponse:
    task = get_object_or_404(models.Task, pk=pk, owner=request.user)
    if request.method == "POST":
        task.delete()
        messages.success(request, _("task deleted successfully"))
        return redirect('task_list')
    return render(request, 'tasks/task_delete.html', {'task': task})
```

URL pattern:

```Python
    path('task/<int:pk>/delete/', views.task_delete, name='task_delete'),
```

and the [template](../tasker_04/tasks/templates/tasks/task_delete.html) for the confirmation, again, fully interchangable with class based view.

To test, just uncomment the delete button in the [task_detail.html](../tasker_04/tasks/templates/tasks/task_detail.html) template.

## Conclusions

Function based views have quite much redundant boilerplate code, however, are a bit more flexible in how things are done, easier to customize. However, such function based views can grow out into spaghetti code very easily.

## Assignment

Implement user permissioned CRUD workflow for one or more models as function based views in your Blog project.
