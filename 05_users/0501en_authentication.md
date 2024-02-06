# User Authentication

Since we are making our TASKer project interactive, we need to handle user authentication. Users must be able to sign up, log in and out of our website. As well as they may want to be able to change some user preferences, maintain their user profile, and manage their credentials. Most of the functionality of user authentication is already implemented in `django.contrib.auth` app, we only need to create HTML templates for the user interface and integrate into our project.

## Objectives

* Create a reusable user profile app.
* Create a user registration form and view.
* Create HTML templates for login / logout and change password workflow.
* Create a user profile page.
* Create user menu in `base.html` header, left of the language picker.

## Creating a reusable user profile app

This is just a reminder of the [0102](../01_new_project_app/0102en_app_config.md). Please repeat all the steps, with these alterations in min:

* name the app `user_profile`.
* URL pattern is `user_profile/`
* app's verbose name is `user profile` 

## User Registration

Django can process forms in two ways. The base way is to manually draw HTML form in the template and process POST data in the view. We have done very similarly with our language picker. When we have more complex data to pass through, we can use Django's form functionality. And in our case, it has even user registration form, which we can inherit, and it will take care of username and password handling mechanics.

So let's create `forms.py` file in our `user_profile` app and import it, then add the fields we need for email, first and last name:

```Python
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

class CreateUserForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'email')
```

Note, that when we use Django's User model in our apps, we always access it through it's getter function `get_user_model`. It is done so, that in case later we would decide to override default user model, we would not break the relationship functionality in any of our apps.

Then we create the view in `views.py`:

```Python
from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from . import forms

def signup(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = forms.CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _("Thank you! You can log in now with your credentials."))
            return redirect("index")
    else:
        form = forms.CreateUserForm()
    return render(request, 'user_profile/signup.html', {
        'form': form,
    })
```

And we use all the best practices we know to create such a view:

* Import User model via `get_user_model` getter function
* Use Django's messages functionality for user feedback.
* Process form data only in case we get it through POST, otherwise render empty form
* Only save form data to model object if the form is valid. Lucky for us, all the validation is handled by the base form.
* If the form is filled correctly, we redirect the user further along it's workflow path. For now it is the index page, but later we will change it to login page once we make it work.

Now let's create URL for the signup page in our `urls.py`:

```Python
from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
]
```

And the HTML template, which we place in, as declared in the view, to `templates/user_profile/signup.html` file:

```HTML
{% extends "base.html" %}{% load i18n %}
{% block title %}{% trans "signup for"|capfirst %} {{ block.super }}{% endblock title %}
{% block content %}
<h1>{% trans "signup for"|capfirst %} TASKer</h1>
<form method="post" action="{{ request.path }}">
    {% csrf_token %}
    {{ form.as_p }}
    <p><button type="submit">{% trans "register"|capfirst %}</button></p>
</form>
{% endblock content %}
```

And we use all the best practices:

* short user strings are all lowercase and use cap manipulation filters where needed, to reduce translatables.
* form action points to itself
* CSRF is utilized

And we can add some CSS styles to improve the layout of our form to `static/css/style.css` in our tasks app:

```CSS

.message, ul.errorlist {
    padding: 0.5rem;
    margin: 0;
    border-bottom: 1px solid #888888;
}

...

.message-error, ul.errorlist {
    background-color: #ffaaaa;
}

...

main form label {
    display: inline-block;
    min-width: 20vw;
    font-size: 120%;
}

main form input, 
main form textarea, 
main form select,
main form button {
    font-size: 120%;
}

main form .helptext {
    display: block;
    font-size: 90%;
}
```

If you still don't like what you see, feel free to adjust it to your liking. This style should persist across all the forms of our app from now on.

## Templates for default user views

First we need to add default Django's User views to our project's `urls.py`:

```Python
urlpatterns = [
    path('', include('tasks.urls')),
    path('user_profile/', include('user_profile.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
]
```

So from now on, the default user functionality views start working in our project, like login, logout, forgot password workflow, etc. But these views do not have templates. Let's create them in our `user_profile` app `templates/registration` folder:

* [Login Form](../tasker_04/user_profile/templates/registration/login.html)
* [Logged Out Message](../tasker_04/user_profile/templates/registration/logged_out.html)
* [Password Reset Form](../tasker_04/user_profile/templates/registration/password_reset_form.html) - the form with email field to send password reminder letter to.
* [Password Reset Form Done](../tasker_04/user_profile/templates/registration/password_reset_done.html) - the message to display after filling the previous form. It will be displayed regardless of the fact that user was found and mail was sent for security purposes.
* [Password Reset Email](../tasker_04/user_profile/templates/registration/password_reset_email.html) - Plain text email message content, containing password reset link.
* [Password Reset Confirm](../tasker_04/user_profile/templates/registration/password_reset_confirm.html) - the form which opens by clicking password reset link from the email.
* [Password Reset Complete](../tasker_04/user_profile/templates/registration/password_reset_complete.html) - the message which confirms successful password reset.

We should also define default login destination URL in project's settings:

```Python
LOGIN_REDIRECT_URL = '/'
```

Since settings are being loaded before any URL pattern reverse functionality, we can only define manual URL patterns here. The line above can be added anywhere, best at the very bottom, before loading in local settings.

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
def user_detail(request: HttpRequest, username: str | None = None):
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

Now we have functioning user self-service functionality on the frontend, including signup, login, logout, password reminder and user profile page. Don't forget translations!
