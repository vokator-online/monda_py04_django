# 3rd party Django apps

This course section will cover some easy to user popular and quite powerful 3rd party Django app packages, which some of them integrate 3rd party products, like TinyMCE rich text editor widget, REST API based combobox widget easy_select2, and Django-Rosetta admin-like interface to manage gettext translations.

Due to big changes in almost all files required from now on, we will continue to work with [tasker_08 project](../tasker_08/).

## Objectives

* Install `django-tinymce` from pip
* Configure `tinymce` app in our project
* Modify the model to use `HTMLField` from tinymce instead of TextField
* Test HTML fields in Django Admin
* Fix HTML field rendering on the frontend
* Update Task and Project forms to include proper widget in the frontend
* Configure rich text editing widget in settings

## Installation

Firstly, we pip install it:

```bash
pip install django-tinymce
```

then we add it to the requirements:

```bash
pip freeze >requirements.txt
```

Now let's configure it to work properly in our projec:

in project's [settings.py](../tasker_08/tasker/settings.py) we add `tinymce` under our apps, but before django apps, inside `INSTALLED_APPS` list.

```Python
INSTALLED_APPS = [
    'tasks',
    'user_profile',
    'tinymce',
    'django.contrib.admin',
    # ...
]
```

And we need URL pattern added inside our [project's urls.py](../tasker_08/tasker/urls.py):

```Python
urlpatterns = [
    path('', include('tasks.urls')),
    path('user_profile/', include('user_profile.urls')),
    path('tinymce/', include('tinymce.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
]
```

## TinyMCE usage in models

It's done. Next let's ammend our models and enable the new functionality for our [models](../tasker_08/tasks/models.py).

```Python
from tinymce.models import HTMLField


class Project(models.Model):
    name = models.CharField(_("name"), max_length=100, db_index=True)
    description = HTMLField(_("description"), max_length=10000, null=True, blank=True)
    # ...


class Task(models.Model):
    name = models.CharField(_("name"), max_length=100, db_index=True)
    description = HTMLField(_("description"), max_length=10000, null=True, blank=True)
    # ...
```

Let's make and run migrations:

```bash
(venv) :~/tasker_08$ ./manage.py makemigrations
Migrations for 'tasks':
  tasks/migrations/0004_project_description_alter_task_description.py
    - Add field description to project
    - Alter field description on task
(venv) :~/tasker_08$ ./manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions, tasks
Running migrations:
  Applying tasks.0004_project_description_alter_task_description... OK
```

And check the changes in Admin while creating or editing a Project or a Task. `ProjectAdmin` class might not have `description` field there, so you will need to add it.

## Rendering HTML fields in templates

Since Django, for security reasons, renders HTML code as text, we need to mark the content of HTML fields as safe. Yes, this is a security compromise - but TinyMCE app mitigates a lot of issues on it's own. For example, JavaScript will not be propagated through.

Example:
```HTML
<div class="user-content">{{ object.description|safe }}</div>
```

Files to fix:

* [project_detail.html](../tasker_08/tasks/templates/tasks/project_detail.html)
* [task_detail.html](../tasker_08/tasks/templates/tasks/task_detail.html)

It is recommended to wrap user content into special divider with class, where we define some boundaries to avoid big mess when users make it happen.

```CSS
.user-content {
    background-color: #ffffff7f;
    border: 2px solid #999999;
    border-radius: 1rem;
    margin: 1rem;
    overflow: auto;
    max-width: max-content;
}
```

## TinyMCE usage in frontend

Now let's make it work as nicely for all the users, not only in Admin. Of course we want to make it work for only authenticated users, and only when form is present on the page, to reduce common loading time. With these conditions in mind, we add `tinymce` scripts into` <head>` tag of the [base.html](../tasker_08/tasks/templates/base.html):

```HTML
...
<head>
    ...
    {% if request.user.is_authenticated and form %}
        <script src="{% static 'tinymce/tinymce.min.js' %}"></script>
        {{ form.media }}
    {% endif %}
</head>
...
```

And now, if field is in the form, it should just work. We may need to add `description` field to the `ProjectCreateView` and `ProjectUpdateView` `fields` tuples in [views.py](../tasker_08/tasks/views.py).

## TinyMCE configuration

We can customize TinyMCE functionality in [settings](../tasker_08/tasker/settings.py). Apparently it is not as tiny as you may thought. Here we provide a simple configuration, of which you can remove things you think should not be left for regular users.

```Python
TINYMCE_DEFAULT_CONFIG = {
    "menubar": "file edit view insert format tools table help",
    "plugins": "advlist autolink lists link image charmap anchor "
               "searchreplace visualblocks code insertdatetime "
               "media table paste help wordcount",
    "toolbar": "undo redo | bold italic underline strikethrough | "
               "fontselect fontsizeselect formatselect | "
               "alignleft aligncenter alignright alignjustify | "
               "outdent indent | numlist bullist checklist | "
               "forecolor backcolor casechange permanentpen "
               "formatpainter removeformat | pagebreak | "
               "charmap emoticons | insertfile image media "
               "pageembed link anchor codesample | "
               "ltr rtl | showcomments addcomment code",
    "custom_undo_redo_levels": 10,
}
```

More configuration options and deep down diving can be done with the official documentation:

* [Official TinyMCE docs](https://www.tiny.cloud/docs/general-configuration-guide/)
* [Django TinyMCE docs](https://django-tinymce.readthedocs.io/)

## Conclusion

Very powerful tool in creative hands, TinyMCE can enable content editing functionality for your users, but should be used with care. Since this solution is publicly available for a very long time already, it is very safe and stable. However, if you don't want your users to visually troll your website, you should disable certain features.

## Assignment

Make your Blog project come to life: enable full featured content publishing for your users by integrating TinyMCE into your Blog project.
