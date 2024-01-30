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
...
from django.utils.translation import gettext_lazy as _
...
def task_done(request: HttpRequest, pk:int) -> HttpResponse:
    ...
    messages.success(request, f"{_('task').capitalize()} #{task.pk} {_('marked as')} {_('done') if task.is_done else _('undone')}.")
    return redirect(task_list)
```

## Generating translation files and translating their contents

In every app which has translatable strings, we need to create `locale` folder. Then we can use `manage.py` command `makemessages` with language/locale argument, for example `-l=lt` for lithuanian language. We will find [django.po](../tasker_04/tasks/locale/lt/LC_MESSAGES/django.po) file in `locale/lt/LC_MESSAGES` folder. We can open them with VS Code and translate their contents.

