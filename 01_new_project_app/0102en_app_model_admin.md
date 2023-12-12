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
    path('', include('tasks.urls')),    
    path('admin/', admin.site.urls),
]
```

And from this moment, the app becomes integral part of our Django project. We can use root (`'/'` or just `''`) url space for our `tasks` app's included urls, but we should avoid using the same url space for different apps.

## Assignemnt

Create the app `pages` for your blog/site project, then create `templates` and `locale` directories for the app, `urls.py` file, add verbose app name to `apps.py` metaclass. Include the app into your project's `settings.py` and include urls into project's `urls.py`. 

Just get familiar with the process. We will be creating many more apps and projects during this course, so you will get proficient. Coming next is data modeling.