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
