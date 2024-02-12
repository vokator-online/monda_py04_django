# Data modeling with Django

Object Relationship Manager is one of the many core Django features. We will use it to do database modeling. For starters, we do not need even basic SQL knowledge to begin modeling. However, we do need basic understanding of related tables and how relational databases do function. We will cover this here.

## Objectives

* Create a simple related model for the use case
* Create and run database migrations
* Register models in Django administration and try it out.

## Use case

For initial part of Django course we will use a simple related model, which we will expand later.

Users will be able to create and manage Tasks and group them into Projects.

Here is the schematic view of the data model. 

![Project-Task-User model](img/project_task_user_model.png)

[DB Designer](https://dbdesigner.net) was used to create this schema. It is a very useful online tool to visualize the data model schema, free for small limited scope projects. 

## Creating models

The most important part of our project is data modeling. If done incorrectly, bad data model will ruin the project no matter how well executed is the rest of the codebase.

Models are always class based.

We will start from the simple app containing a user related `Project` and `Task` models in `tasks/models.py` file.

`Project` has just a `name` field and a user related `owner` field.

`Task`, in addition, contains a `project` field, which relates to `Project` model, a text field `description`, `created_at`, `updated_at` fields for time tracking, and the `is done` boolean field to track it's completion status.

```Python
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _


class Project(models.Model):
    name = models.CharField(_("name"), max_length=100, db_index=True)
    owner = models.ForeignKey(
        get_user_model(), 
        on_delete=models.CASCADE, 
        verbose_name=_("owner"), 
        related_name='projects',
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("project")
        verbose_name_plural = _("projects")
        ordering = ['name']

    def get_absolute_url(self):
        return reverse("project_detail", kwargs={"pk": self.pk})


class Task(models.Model):
    name = models.CharField(_("name"), max_length=100, db_index=True)
    description = models.TextField(_("description"), blank=True, max_length=10000)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE, 
        verbose_name=_("project"), 
        related_name='tasks',
    )
    owner = models.ForeignKey(
        get_user_model(), 
        on_delete=models.CASCADE, 
        verbose_name=_("owner"), 
        related_name='tasks',
    )
    created_at = models.DateTimeField(_("created at"), auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True, db_index=True)
    is_done = models.BooleanField(_("is done"), default=False, db_index=True)
    deadline = models.DateTimeField(_("deadline"), null=True, blank=True, db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("task")
        verbose_name_plural = _("tasks")
        ordering = ['is_done', '-created_at']

    def get_absolute_url(self):
        return reverse("task_detail", kwargs={"pk": self.pk})
```

As you see, we have created a one-to-many relationship between the `Project` and `Task` models, meaning that each task will belong to one project, while a project can have zero to many tasks. We will be able to access all project's tasks through `.tasks` attribute of the project's object, since we have defined a related name.

Special attention to `owner` field, which is a foreign key to Django's `contrib.auth` app's `User` model. We use `get_user_model` function to get user model, making our app compatible with custom user models by executing our model relationship this way. Since we done it from both models, and defined related names respectively, we will be able to reach both datasets from `user` object. About that later in the course.

We also have created some time tracking fields. `created_at` will get it's value set only when the task object is created, while `updated_at` will be reset every time the object is updated. We have added optional field `deadline`, which is not required, but a nice to have quality of life feature in case we want to set deadlines for tasks.

Note here, that we have made `name`, `created_at` and `updated_at`, `is_done` and `deadline` fields indexed in our database. That will greatly increase performance when searching and sorting our tasks, and insignificantly reduce performance while creating such tasks.

The final remark is regarding primary key field by default named `id` and of type `integer` which is set to auto incremental value. Since version 4.0, Django handles it automatically. We can refer to such field within Django as to both `id` and `pk` (meaning Primary Key). `_id` suffixes for foreign key fields are also handled since Django ORM inception so you don't need to add them to related field names. 

### Creating and running migrations

Every time app's model is updated, we should create and run migrations. We can do so by performing these commands in our terminal.

```bash
./manage.py makemigrations
./manage.py migrate
```

While executing `makemigrations`, Django will check for changes across all our project apps and create migration files where any changes were detected. We can pass app name as an argument to the command. Then, `migrate` will just execute the changes. To check project's migration status, we can use `showmigrations` management command.

If you check the example of this course material `tasker`, you will find that the `deadline` field for the `Task` model class is migrated in `0002_` migration. It is done on purpose to demonstrate how painless it is to add features to your model when your application scope scales up.

## Registering your models to Django Administration

To be able to manipulate our app's model objects with Django administration, we need to register our model to it. That is done in the `tasks/admin.py` file:

```Python
from django.contrib import admin
from . import models

admin.site.register(models.Project)
admin.site.register(models.Task)
```

Now you can run the server and play with your projects the tasks.

## Assignments

1. Create a few projects and tasks for the superuser. Then create another user, give that user all permissions related to the models, then log into Admin with that user and try to create/update/delete some projects/tasks. Note that you can manipulate all objects regardless of their ownership. It is because Django permissions are model level, not object level. We will use object level permission logic later when creating the frontend of our app, and we will focus on making our Django Administration for our app more useful and pretty in the next section.

2. Create a model `Page` for your blog/site project, related to another new model `Category`. Think about what fields do you want to have there, what data about such pages should be stored in the database. Pages also should be user related. Register the admins, and add some content, get the grip of the overall process. Don't overhtink and overcomplicate things. Just remember that we did not start with the frontend yet.

---
Don't focus too much on Administration part yet, just make sure the models work as intended. Next we are going to take on Django Administration and adapt it's many great features to help manipulate our models and look it all pretty.
