# Static Files, Styling and Base Layout

So far our application style looks and feels like a typewriter draft. Let's make it modern app style and actually useful and good looking. For that we need to design the app layout, and we will need to bring up CSS (Cascaded Style Sheets) functionality in our templates.

## Objectives

* Configure Static Files for Django Project
* Create `style.css` base static file for our base template
* Modify the layout of `base.html` and style it to look app-like and human-usable
* Create styles for most commonly used cases in our app, for example lists, links, etc.

## Static and User Files in Django

Static files are mostly set up in Django already, the only things left to do are to create static folders for apps themselves, decide on file/folder naming convention and add path to URL in project's `urls.py`. First, we determine physical location of compiled static files for the project in `settings.py`:

```Python
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR.joinpath(STATIC_URL)
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR.joinpath(MEDIA_URL)
```

At the same time we do this also for the media files, which usually are user uploaded files (including `admin` users). We will need MEDIA later.

The parameter name is `STATIC_ROOT`, and the recommended value is `BASE_DIR` path plus the value of `STATIC_URL`. Also same goes for the `MEDIA_ROOT`.

Then we modify the __project's__ `urls.py` file, by importing `static` from `django.conf.urls.static` and adding it's result to the `urlpatterns`.

```Python
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('tasks.urls')),    
    path('admin/', admin.site.urls),
]

urlpatterns.extend(static(settings.STATIC_URL, document_root=settings.STATIC_ROOT))
urlpatterns.extend(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
```

From now on, we can use `FileField` or `ImageField` fields in our models, and users (or admins) could upload files related to the data models. We will get there soon enough. But now let's take one step at a time and do some app styling.

## Base template styling

Let's create `static/css/style.css` file in our `tasks` app. Create necessary folders along the way:

```CSS
body {
    background-color: #cccccc;
    font-family: sans-serif;
    font-size: 16px;
}
```

We just added one basic instruction for page body, defining a default typography and a grey background, in this case to recognize that the style itself is working once background color changes. Later we can change color theme to our liking.

Let's include this style file into our base template:

```HTML
<!DOCTYPE html>
<html lang="en">
{% load static %}
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}TASKer{% endblock title %}</title>
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
</head>
...
```

We should load django template tags as early as possible, but in case of base template, we should not do it before `<html>` tag. Then, we add `<link rel href>` element to `<head>`.

Time for testing. The font should become different and background should be grey. If it doesn't work, remember to restart the server.

## Base Layout

Instead of using CSS frameowrks, it is much easier today to just write a clean style from scratch, since CSS has improved in modern browsers so much, it works much faster and is really less code to maintain and looks cleaner at the end. For the sake of knowledge, we will implement both concepts of layout, `grid` and `flex`, through-out our app.
The main layout will be `grid`, while inner layouts will be `flex`. More on both of these layout concepts: [grid](https://css-tricks.com/snippets/css/complete-guide-grid/) and [flex](https://css-tricks.com/snippets/css/a-guide-to-flexbox/).

