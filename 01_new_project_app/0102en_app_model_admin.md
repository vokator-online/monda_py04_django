# Creating the `Tasks` app in our `Tasker` django project

## Objective
In this section, we will create the `tasks` app, define the `task` model, and integrate it with the Django admin interface.

## Let's create the app

Open the terminal and make sure that your virtual environment is activated and you are in the `tasker` directory with `manage.py` file. If you see `(venv)` on the left of the command prompt, venv is activated. You can verify your current location by using `pwd` and `ls` bash commands. `pwd` means `print working directory`. You should see `manage.py` file in the result of the `ls` command.

Then run:
```bash
./manage.py startapp tasks
```

The app directory will be created with the skeleton of the app files in there, which is best explained by MVT architecture.

## Understanding MVT Architecture

MVT stands short for Model-View-Template. 

![MVT Architecture](img/mvt_architecture.png)

The user creates the **request** over a web browser through URL, which is processed via `urls.py` and corresponding view from `views.py` is executed, which interfaced with **models** at `models.py` and **renders** the resulting **template** located in `templates` directory. 

* `models.py` will contain our data models, which we will registar into Django Administration in `admin.py` file.
* `migrations` directory will include all the model migration scripts.
* `views.py` will contain the views, which will render HTML templates to be placed into `templates` directory to be created.
* `tests.py` file is for unit tests of the models.
* We also need to create `locale` directory which will hold `gettext` translation files.
* `__init__.py` files are intentionally empty in all directories, which are considered a Python package. 
* And finally, we will create `urls.py` file with a few lines:

```Python
from django.urls import path

urlpatterns = []
```

It is an empty URLs file template, which imports the `path` function from `django.urls`, and we will fill `urlpatterns` list with a list of that `path` results when adding views and URLs for our app.

---

`apps.py` contains the app controller class, to which we will add another subclass `Meta`, where we will add a translatable verbose name of the app.

```Python
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class TasksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tasks'

    class Meta:
        verbose_name = _('tasks')
```

Here pay attention to how did we import multilingual **gettext** functionality. We will use **gettext** this way across the app, including but not limited to apps, models, views, etc. Only in templates it is done differently.

## Registering our app into `tasker` Django project

In `settings.py` file of our `tasker` project, we add `tasks` app name to the top of the `INSTALLED_APPS` list.

```Python
INSTALLED_APPS = [
    'tasks',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```

Then, in `urls.py` file of our `tasker` project (NOT app's `urls.py` file), we need to include our app's URLs.

```Python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('tasks/', include('tasks.urls')),    
    path('admin/', admin.site.urls),
]
```

And from this moment, the app becomes integral part of our Django project.

## Creating a model

The most important part of our project is data modeling. If done incorrectly, bad data model will ruin the project no matter how well executed is the rest of the codebase.

Models are always class based.

We will start from the simple app containing a user related `Project` and `Task` models in `tasks/models.py` file.

`Project` has just a `name` field and a user related `owner` field.

`Task`, in addition, contains a `project` field, which relates to `Project` model, a text field `description`, `created_at`, `updated_at` fields for time tracking, and the `is done` boolean field to track it's completion status.

```Python
from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model


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

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("task")
        verbose_name_plural = _("tasks")
        ordering = ['is_done', '-created_at']
```

As you see, we have created a one-to-many relationship between the `Project` and `Task` models, meaning that each task will belong to one project, while a project can have zero to many tasks. We will be able to access all project's tasks through `.tasks` attribute of the project's object, since we have defined a related name.

Special attention to `owner` field, which is a foreign key to Django's `contrib.auth` app's `User` model. We use `get_user_model` function to get user model, making our app compatible with custom user models by executing our model relationship this way. Since we done it from both models, and defined related names respectively, we will be able to reach both datasets from `user` object. About that later in the course.

Time tracking fields like `created_at` will get it's value set only when the task object is created, while `updated_at` will be reset every time the object is updated.

Note here, that we have made `name`, `created_at` and `updated_at`, and `is_done` fields indexed in our database. That will greatly increase performance when searching and sorting our tasks, and insignificantly reduce performance while creating such tasks.

The final remark is regarding primary key field, by default named `id` and of type `integer` which is set to auto incremental value, that Django handles it automatically. We can refer to such field within Django as to both `id` and `pk` (meaning Primary Key).

### Creating and running migrations

Every time app's model is updated, we should create and run migrations. We can do so by performing these commands in our terminal.

```bash
./manage.py makemigrations
./manage.py migrate
```

While executing `makemigrations`, Django will check for changes across all our project apps and create migration files where any changes were detected. We can pass app name as an argument to the command. Then, `migrate` will just execute the changes. To check project's migration status, we can use `showmigrations` management command.

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

2. Create an app `Pages` with a model `Page` for your blog/site project, related to another model `Category`. Think about what fields do you want to have there, what data about such pages should be stored in the database. Register the admins, and add some content, get the grip of the overall process. Don't overhtink and overcomplicate things. Just remember that we did not start with the frontend yet.
