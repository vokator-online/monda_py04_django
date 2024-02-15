# Translations

Django supports multilingual web application development right out of the box for the user interface, which we will discover in this section. Database architecture adaptation for multilingual use, on other hand, is left to the app developer. We will NOT touch the multilingual DB architecture aspect.

## Objectives

* Check how python code is marked for translation in models of our app.
* Generate locale files with `makemessages` django command for chosen language(s).
* Translate strings in `django.po` files
* Complile translations with `compilemessages` django command into `django.mo` files
* Change default Django language and test the translations
* Add translation functionality in HTML templates and translate user interface related strings from there

## Translation in python files

In order to make user directed strings translatable, we import `gettext` or `gettext_lazy` from `django.utils.translation` as `_` function and use it in our code to wrap any translatable text. And that is it, all texts which go through our `_` function in python are ready for translation. The examples are in `models.py` and `admin.py` files of our app already, as well as one verbose value in `apps.py`.

We have one line full of translatable strings in `views.py` file which is not translated - the message when we update task status. Let's fix that:

```Python
# ...
from django.utils.translation import gettext_lazy as _
# ...
def task_done(request: HttpRequest, pk:int) -> HttpResponse:
    # ...
    messages.success(request, "{} {} {} {}".format(
        _('task').capitalize(),
        task.name,
        _('marked as'),
        _('done') if task.is_done else _('undone'),
    ))
    return redirect(task_list)
```

Note here that so called `f""` string is not working correctly with gettext and so with Django's `makemessages` command, so we are forced down to use `.format()` string method instead.

## Generating translation files and translating their contents

In every app which has translatable strings, we need to create `locale` folder. Then we can use `manage.py` command `makemessages` with language/locale argument, for example `-l=lt` for lithuanian language. We will find [django.po](../tasker_04/tasks/locale/lt/LC_MESSAGES/django.po) file in `locale/lt/LC_MESSAGES` folder. We can open them with VS Code and translate their contents.

If you get an error that gettext is not found and required, you can install it with apt:

```bash
(venv) bash:~/$ sudo apt install gettext
```

...and then the `django makemessages -l=lt` command above should work. In some cases reloading the terminal, VS Code or even WSL might be required if it doesn't. 

For macOS, install with brew or ports, and reboot is required.

Then, once translations are ready, we need to compile them by running `manage.py` command `compilemessages`.

```bash
(venv) bash:~/monda_py04_django/tasker_04$ ./manage.py compilemessages
processing file django.po in /home/kestas/monda_py04_django/tasker_04/tasks/locale/lt/LC_MESSAGES
```

## Project's Language Settings

We can change default project's language in project's `settings.py` file, by setting `LANGUAGE_CODE` value.

```Python
LANGUAGE_CODE = 'lt'
```

Then after restarting the server we can see the translated results. There is nothing translated on the frontend (yet), but we can see the difference in `admin`.

## Translations in HTML templates

We can mark text for translation in HTML templates by passing it through `{% trans %}` tag as string argument. Let's translate the `base.html` template.

First, we make sure the internationalization HTML tags library called `i18n` is loaded.

```HTML
<!DOCTYPE html>
<html lang="en">
{% load static i18n %}
...
```

When it comes to content, only menu items had translatables.

```HTML
<ul class="nav">
    <li><a href="{% url 'index' %}">{% trans "dashboard"|capfirst %}</a></li>
    <li><a href="{% url 'task_list' %}">{% trans "tasks"|capfirst %}</a></li>
</ul>
```

There are a few translatables in `index.html`:

```HTML
{% extends "base.html" %}
{% load i18n %}
{% block content %}
    <h1>{% trans "dashboard"|capfirst %}</h1>
    <p>{% trans "users"|capfirst %}: {{ users_count }}</p>
    <p>{% trans "projects"|capfirst %}: {{ projects_count }}</p>
    <p>{% trans "tasks"|capfirst %}: {{ tasks_count }}</p>
{% endblock content %}
```

Note: Make sure not to forget loading the `i18n` library.

Then, we do the same for other templates (`task_list.html` and `task_list.html`).

Once translatables are defined for the HTML templates:

* regenerate translation file with `makemessages` management command
* go through text translations in the translations file, located in app's `locale` folder
* run `compilemessages` management command

Congratulations, the UI is now translated! Next, we are going to create a language switcher widget for the frontend user interface, and language detection for our Django project.

## Assignment

Create translations for your blog project user interface, do the translations, and test. Choose the language other than English you are proficient with.
