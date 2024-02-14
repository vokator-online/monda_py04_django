# Mark task done/undone view

Let's create one more view, this time a redirect view, which just changes the status of the task. In this case - marks task done if it was not done, and undo if it was.

## Objectives

* Mark selected task done/undone
* Display user notifications via Django's messages in Templates in case the task done status has changed.

The view is a bit different, as we do the changes to the object of the queried `Task`, and then redirect it to `task_list` view, and we need to import `redirect` from `django.shortcuts` as well:

```Python
def task_done(request: HttpRequest, pk:int) -> HttpResponse:
    task = get_object_or_404(models.Task, pk=pk)
    task.is_done = not task.is_done
    task.save()
    return redirect(task_list)
```

And the URL pattern line is very similar to the `task_detail`:

```Python
urlpatterns = [
    # ...
    path('task/<int:pk>/done/', views.task_done, name='task_done'),
]
```

Now just fix the `tasks/task_list.html` template where we add the link on the checkbox itself:

```HTML
<li><a href="{% url "task_done" task.pk %}">
    {% if task.is_done %}&#x2611;{% else %}&#x2610;{% endif %}</a>
    <a href="{% url "task_detail" task.pk %}">{{ task.name }}</a>
    <span style="float:right;">{{ task.deadline }}</span>
</li>
```

## Django Contrib Messages

While the page is not too crowded with tasks and light, it might seem that the mark changes in real time and the page is not even re-drawn. Still, we want to let user know if the operation was performed. We can do that with `django.contrib.messages` functionality, which is very easy to use.

Let's import them at the top of our `views.py`:

```Python
from django.contrib import messages
```

Then add the `messages.success()` to the view before `return`:

```Python
def task_done(...):
    # ...
    messages.success(request, f"Task #{task.pk} marked as {'done' if task.is_done else 'undone'}.")
    return redirect(task_list)
```

And we need to create the notifications section in the `base.html` file, that all messages could be displayed on any page rendered next of the message event:

```HTML
    ...
    </header>
    <section class="messages">
        {% for message in messages %}
            <p class="message message-{{ message.tags }}">{{ message }}</p>
        {% endfor %}
    </section>
    <main> ...
```

Now the message will be displayed whenever the message will be marked done or undone. It looks too raw for our liking, but for now it is important to just make it work. The point is, that with this little amount of code we can make it work. Then, we take care of the styling. And just before we do that, why not to make that marking done work from the detail view as well? The only change needed there is to add the link around the checkboxes logic in `list_detail.html`. However, we add the `next` GET variable to the URL, which values to the current page:

```HTML
...
<h1><a href="{% url "task_done" task.pk %}?next={{ request.path }}">
    {% if task.is_done %}&#x2611;{% else %}&#x2610;{% endif %}</a>
    {{ task.name }}</h1>
...
```

So we can check for it in the `task_done` view, and it it is set, redirect to the value instead. This makes user experience much smoother with very little effort on coding side, because when user uses `mark_done` view, it redirects back to the detail view. Final code of the `task_done` view:

```Python
def task_done(request: HttpRequest, pk:int) -> HttpResponse:
    task = get_object_or_404(models.Task, pk=pk)
    task.is_done = not task.is_done
    task.save()
    messages.success(request, f"Task #{task.pk} marked as {'done' if task.is_done else 'undone'}.")
    if request.GET.get('next'):
        return redirect(request.GET.get('next'))
    return redirect(task_list)
```

## Assignment

If you have no boolean type fields in your blog app's model, consider creating `is_published` field for the blog. Then you can replicate the functionality by switching that variable.
