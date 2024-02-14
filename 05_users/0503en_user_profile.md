## User Profile Page

Let's create a simple user detail page, displaying user's first and last name and username. We will populate the page later in the course with more functionality and statistics.

The view, including updated imports:

```Python
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext_lazy as _
from . import forms

User = get_user_model()

@login_required
def user_detail(request: HttpRequest, username: str | None = None)  -> HttpResponse:
    if username:
        user = get_object_or_404(User, username=username)
    else:
        user = request.user
    return render(request, 'user_profile/user_detail.html', {
        'object': user,
    })
```

Here again we use best practices, minimizing the code used to achieve results and avoiding errors:

* `login_required` decorator redirects unauthenticated users to login. This page will only be accessible to logged in users.
* If user by the username is not found, the 404 page will be displayed. We will customize project's error page templates later in the course.
* If username is not provided, currently logged in user's details page will be rendered instead.

Then we create two URL patterns - one with username argument, another without:

```Python
urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('detail/', views.user_detail, name='user_detail_current'),
    path('detail/<str:username>/', views.user_detail, name='user_detail'),
]
```

And then we just finish with the template of `user_profile/user_detail.html`:

```HTML
{% extends "base.html" %}{% load i18n %}
{% block title %}{{ object }} {% trans "at" %} {{ block.super }}{% endblock title %}
{% block content %}
<h1>User {{ object.username }}</h1>
<p>{{ object.first_name }} {{ object.last_name }}</p>
{% endblock content %}
```

Now we have everything we need for user related frontend functionality of our project.

## User Menu

Let's link all that nice user functionality to the user menu in the `base.html`, between the spacer and language picker:

```HTML
...
<span class="spacer"></span>
<ul class="nav nav-user">
    {% if user.is_authenticated %}
        <li><a href="{% url 'user_detail_current' %}">{{ user }}</a></li>
        {% if user.is_superuser or user.is_staff %}
            <li><a href="{% url 'admin:index' %}">{% trans "admin"|capfirst %}</a></li>
        {% endif %}
        <li><form method="post" action="{% url "logout" %}">{% csrf_token %}<button type="submit">{% trans "log out"|capfirst %}</button></form></li>
    {% else %}
        <li><a href="{% url 'login' %}">{% trans "log in"|capfirst %}</a></li>
        <li><a href="{% url 'signup' %}">{% trans "sign up"|capfirst %}</a></li>
    {% endif %}
</ul>
...
```

User authentication logic is implemented here, where authenticated users are shown their profile page link and option to log out, and staff or superuser users get also "Admin" link. Unauthenticated users get login and signup links.

## Conclusion

Now we have functioning user self-service functionality on the frontend, including signup, login, logout, password reminder and user profile page. Don't forget translations!

Profile editing and User model extension we will cover after generic CRUD view course.

## Assignment

Copy the just created user_profile app to your blog project and integrate it:

* add necessary configuration lines to `settings.py`
* add necessary URL patterns to project's `urls.py`
* change branding in template's strings
* add user menu to `base.html` template
