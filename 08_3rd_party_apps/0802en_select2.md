# Django-Select2

To enable searchable related objects in forms, for better user experience, instead of preloading all available related model entries to form `<select>` tag options, it is much better to use asynchronious loading by query. Javascript AJAX feature is very handy here. And Django utilizes this very concept by using Select2 Javascript library integration.

## Objectives

* Refactor some of our views and forms to use Select2 widget.
* Use `autocomplete_fields` in Admin for models with Foreign Keys.

## Installation

First, we need to install Django-Select2 Python package:

```
pip install django-select2
```

Do not forget to update your requirements file.

And add it to INSTALLED_APPS in [settings.py](../tasker_08/tasker/settings.py) in our app list _after_ `django.contrib.admin` app:

```Python
INSTALLED_APPS = [
    # ... our apps ...
    'django.contrib.admin',
    # ... other Django apps
    'django_select2',
    # ... should be last
]
```

Next, URL patterns need an entry in our project's [urls.py](../tasker_08/tasker/urls.py) file:

```Python
urlpatterns = [
    # ...
    path('select2/', include('django_select2.urls')),
    # ...
]
```

It is also worth noting, that when scaling to multi-thread deployment, **persistent** cache backend is required across all servers or server threads, so `LocMemCache` used by default will not suffice. For the case of our course it is not an issue and it is out of scope. The solution here is `redis` in-memory database for caching and `django-redis` integration.

[Official django-select2 documentation](https://django-select2.readthedocs.io/en/latest/) can be used for reference.

