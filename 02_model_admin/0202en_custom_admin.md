# Customizing Django Admin | Part 1

By just registering models to Django Administration, we get a default model admin functionality. Model representation is `__str__` it's property, fields and their ordering in the create/change view is determined by the model code. We can extend on that.

## Objectives

* Customized representation in model admin's list view
* Admin List Filters
* Admin List Search
* Admin List Editing
* Customized fieldsets in the change form
* Custom funcion representations in model admin's list view

## Defining a custom Model Admin class

In app's `admin.py` file, we will create custom Model Admin classes for our models, and add them as arguments to where they are registered. The updated `admin.py` file should look like this now:

```Python
from django.contrib import admin
from . import models


class ProjectAdmin(admin.ModelAdmin):
    pass


class TaskAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Project, ProjectAdmin)
admin.site.register(models.Task, TaskAdmin)
```

For now, in practice, nothing changed, because these classes are identical to the default ModelAdmin class. Let's improve on that.

## Customizing the appearance of List View

First let's make the list view more pretty. Instead of just `__str__` representation of each record, we want a multi-column table representation, with sortable columns. This, surprisingly, can be achieved just with one line - definition of `list_display`. We can use list or tuple for the list of field names, which we want to be displayed in the table. They will become sortable by default, and if in model we have devined ordering, they default sorting will be taken from there.

Let's do this for both `ProjectAdmin` class:

```Python
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'owner']
```

Go and test it out. 

---

### Quick Assignment 1

Create a list display representation for `TaskAdmin` class. You don't need the ID, but add most relevant fields like `project`, `created_at`, `is_done`. Think about the order. Also avoid huge value fields like `description`.

---

Now you have noticed in `ProjectAdmin` we have used `ID` field just for the kicks to see it's value. However, because we have put `ID` before the `name`, we can only go to detail/change view if we click on the ID of the specific project. We can change this behavior by defining `list_display_links`, which also is an iterable:

```Python
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'owner']
    list_display_links = ['name']
```

You can also leave `id` in the `list_display_links`. Try it out.

## List Filters

While Django Administration is a tool designed not for end-user, but for internal administration, it does not mean administration user interface cannot be optimized for convenience. Filtering is one of such conveniences. Let's add filtering by `project`, `owner`, `is_done`, `deadline`, and `created_at`. All 4 filters, one line:

```Python
class TaskAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_done', 'deadline', 'project', 'owner', 'created_at']
    list_filter = ['is_done', 'project', 'owner', 'deadline', 'created_at']
```

You might not see filters exposed in case of too few data. You should add more Users and Projects to expose their filters. Django is optimized to hide unnecessary bits in case they are not relevant. You should also keep this philosophy in your software architecture.

---

### Quick Assignment 2

Create the `owner` filter in `PorjectAdmin` class.

---

## List search

Filters are convenient as long as they are small. Once we have many projects or users, making search functionality for the filter rather than list filters themselves by those fields would be more productive and convenient. And yes, it's again one added line:

```Python
class TaskAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_done', 'deadline', 'project', 'owner', 'created_at']
    list_filter = ['is_done', 'deadline', 'created_at']
    search_fields = ['name', 'description', 'project__name', 'owner__last_name', 'owner__username']
```

We have removed `project` and `owner` from list filters, and in addition to task's `name` and `description`, we have added search options for `project` and `owner`. However, to avoid searching related entities by their IDs, we can define related field lookups. Related field lookups are constructed by inserting `__` (two underscores) between field names. So if we want, for example, to search owner by his last name and username, we define two lookups, `owner__username` and `owner__last_name`.

---

### Quick Assignment 3

Create search for the `name` in `PorjectAdmin` class.

---

## In-place editing

We can make multi-line editing right in the list view, also for convenience. However, we should be very selective which fields we allow to edit. For example, we should not allow to edit Foreign Key fields just because every line will form a choices widget from the related model data, and that will hurt performance. But it has it's user, for example, `is_done` field for the `TaskAdmin`.

```Python
class TaskAdmin(admin.ModelAdmin):
    # ...
    list_editable = ['is_done']
```

Once we have made changes to the task states (marked them done or undone) in the browser, we need to submit the form (clisk **Save** button). 

## Customized fieldsets in the change form

Now check what is missing in the change view of the, for example, task. Where are `id`, `created_at` and `updated_at` fields? What if we want to change order of some fields, and group some other fields to a single line? We can do all that with a single definition of `fieldsets`. However, it probably is not wise to try fitting it in a single line anymore, as it is multi-dimensional dictionary construct. In fieldsets we first define sections, into which we can group fields. If we take a few fields into one more level of brackets `()`, they will be represented in the same horizontal row. Then, we need to define fields which should not be editable as `readonly_fields` as well.

Section names should be translatable strings, so we pass them trhough imported `gettext_lazy`. We have done this before with models. Just add this import line to the top of `admin.py` file.

```Python
from django.utils.translation import gettext_lazy as _
```

Let's do the fieldsets for `TaskAdmin`:

```Python
class TaskAdmin(admin.ModelAdmin):
    # ...
    readonly_fields = ['id', 'created_at', 'updated_at']
    fieldsets = (
        (_("general").title(), {
            "fields": (
                ('name', 'deadline'),
                'description', 'is_done',
            ),
        }),
        (_("ownership").title(), {
            "fields": (
                ('owner', 'project'),
            ),
        }),
        (_("temporal tracking").title(), {
            "fields": (
                ('created_at', 'updated_at', 'id'),
            ),
        }),
    )
```

It looks complicated, but it isn't if following the identation properly. VS Code also helps to follow the hiearchy by color-differenciation of brackets. To simplify the fieldset's structure, you can leave everything in a single section, remove section labels if you don't need them, etc. Alternatively, if you want to just define field ordering, you can just use `fields` instead of `fieldsets`.

---

### Quick Assignment 4

Create a simple fieldset for `ProjectAdmin`, single section, leave section name as `None`, and add all fields, including `id`, into the same line.

---


## Custom funcion representations in model admin's list view

We can also create custom model list view fields to fetch data from related models. For example, we can count tasks for each Project (total, done and undone even). Or we can list names of a few most recent tasks. For that we need to define a method for the model's Admin class, and use that method's name in `list_display`. Luckily, we have defined `related_name` for `project` field in `Task` model, now it will become useful when returning the result. The implementation is not as complex as it sounds, one-liner the Python way, as intended: 

```Python
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'total_tasks', 'owner']
    list_filter = ['owner']
    list_display_links = ['name']

    def total_tasks(self, obj: models.Project):
        return obj.tasks.count()
    total_tasks.short_description = _('total tasks')
```

As you have probably noticed, I have added list filter for `owner` and stuffed `name` into `search_fields`. Also, if we set `short_description` attribute for the method, it will be used as a column name instead of the "tech_jargon_non_human_friendly" method name.

Now let's do one more method for the tasks undone.

```Python
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'total_tasks', 'undone_tasks', 'owner']
    # ...

    def undone_tasks(self, obj: models.Project):
        return obj.tasks.filter(is_done=False).count()
    undone_tasks.short_description = _('undone tasks')
```

to filter out tasks before counting them, we just used Django ORM's `filter()` function and passed the filtering condition as arugment. Yes, it's that simple, even fits into the same line.

We can do more than just count. We can do anything with related model data here, or anywhere in Django as you will soon find out. Let's retrieve some most recent task names for example:

```Python
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'total_tasks', 'undone_tasks', 'recent_tasks', 'owner']
    # ...

    def recent_tasks(self, obj: models.Project):
        return "; ".join(obj.tasks.order_by('-created_at').values_list('name', flat=True)[:3])
    recent_tasks.short_description = _('recent tasks')
```

That line is a bit to unpack. So we take `obj`'s `tasks` and order them by `created_at`. Then, we take `vaules_list` of `name` field values and make if flat. Then slice it to max 3 entries, to avoid extra-long columns (imagine that there can be 1000s of tasks per project). And to neatly represent such a values list, we use native Python string `join` method on the semicolon-space separator.

---

### Quick Assignemnt 5

Now for a quick practice, try to make a custom field for a short list of most recent undone tasks.

---

## Assignments

1. Create a few more projects, then a lot more tasks. Play with the scenarios. If you run out of ideas, you are welcome to just go and talk to everyone else in the group. You can make your study plan into a tasks-project, as well as starting a company project, or some software project you have ideas for a long time. At least one project should get like 20ish tasks, and there should be over 10 projects, even if some empty. We will need this data to play with during next course.

2. Create more sophisticated administration for your categorized pages. Think about what functionality would allow administrator to manage the ever-growing blogging platform? How would you filter? Is there any field worth making inline editable? What statistics of pages could Category admin use?

#### TODO:
* run through spelling and grammar, also through ChatGPT for suggestions
* add assignments for the blog project
