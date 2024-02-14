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

### Main page layout - Flex

Since our main page layout is one dimentional single column (no permanent sidebar menus, banner spaces, etc.), there is no point to initiate grid. Flexbox is enough, and we better follow keep it simple principle where we can.

For the sake of layout purposes we will also add a footer block to the base template, and set the "read only" block under it with hardcoded copyright message.

```HTML
    ...
    <main>{% block content %}{% endblock content %}</main>
    <footer>
        {% block footer %}{% endblock footer %}
        <p>&copy; 2023-2024 <a href="http://gka.lt" target="_blank">Gero Kodo Akademija</a></p>
    </footer>
</body>
</html>
```

Now we have a challenge that this footer hangs right under the content. It will be especially ugly once we start distinctively coloring the sections. For the purpose of design/color neutrality, we will try to keep greyscale with vivid color accents theme.

So here is the initial version of `style.css` for the basic page layout with header menu section, main content block, and footer:

```CSS
body {
    background-color: #cccccc;
    font-family: sans-serif;
    font-size: 16px;
    display: flex;
    flex-direction: column;
    margin: 0; padding: 0;
    min-height: 100vh;
}

header {
    background-color: #999999;
}

main {
    flex-grow: 1;
}

footer {
    background-color: #666666;
}
```

With `flex-grow: 1` on `<main>` element we make sure the main content block will expand relative to header and footer, and `min-height: 100vh` on `<body>` defines that `<body>` expands to at least full screen height.

### Making links prettier

Default browser colors for links are very ugly blue of violet for visited, with even uglier underline. Let's immediately address that, and make links more intuitive also by defining their hover behavior.

```CSS
a {
    color: #004488;
    text-decoration: none;
}

a:hover {
    color: #0055cc;
}
```

### Menu bar with logo

For top page bar, it is almost always horizontal menu with logo on the left. Mobile version has a burger, but we can address that much later. For now let's define a basic flexbox in flexbox style for the menu items list, with logo on the left.

```CSS
header {
    background-color: #999999;
    display: flex;
    flex-direction: row;
}

header .logo {
    font-size: 24px;
    font-weight: 600;
    padding: 0.5rem;
}

header ul.nav {
    display: flex;
    flex-direction: row;
    list-style-type: none;
    margin-block: 0.5rem;
    padding-inline: 0;
    gap: 1px;
}

header ul.nav li a, header ul.nav li form button {
    background-color: #aaaaaa;
    display: block;
    margin: 0;
    padding: 0.5rem;
    border: none;
    border-bottom: 2px solid #004488;
    cursor: pointer;
    color: #004488;
    font-size: 100%;
}

header ul.nav li a:hover, header ul.nav li form button:hover {
    background-color: #b8b8b8;
    border-bottom: 2px solid #0055cc;
    color: #0055cc;
}
```

As you see, we have taken care of button hover behavior as well. By making links as blocks and expanding to the whole area of the list item has it's benefits not only for touch screens, but also for more visual flexibility, as example, using partial border as button accent. We have also styled form buttons in case we need them as menu links.

### The box model

We also need to understand the basic box theory of HTML element styling: every HTML element is essentially a box, around which goes `padding`, then goes `border`, and then `margin`. Element size includes border and padding and excludes margin. Margins of adjacent elements are overlapping.

### Styling content and generic elements

Now we have a big decision to make how we plan to style our elements in terms of their relative spacing. Paddings on every element are more tedious than on their containers, but such tediousness gives more flexibility, especially when we want to style backgrounds of such elements, or extend them to overlap. So we will use the methodology of padding each element, including inline images, headings, paragraphs, lists in content, etc.

```css
h1, h2, h3, h4, h5, h6 {
    background-color: #bbbbbb;
    border-bottom: 1px solid #888888;
    padding: 0.5rem;
    margin: 1rem 0;
}

p, main ul {
    padding: 0 0.5rem;
    margin: 1rem 0;
}

main ul li {
    border-bottom: 1px solid #999999;
}
```

Another thing which we can use is make headings on top of the page not to be detached from the menu-bar, since that empty whitespace creates no aesthetic value and wastes space.

```CSS
h1:first-child, h2:first-child, h3:first-child, 
h4:first-child, h5:first-child, h6:first-child {
    margin-top: 0;
}
```

### Styling footer

Even if our footer is not very big yet, still the text there looks not so legible and unprofessional. Let's make the text to contrast from the dar background for both paragrapth and links in it:

```CSS
footer p {
    color: #cccccc;
}

footer a {
    color: #66aaff;
}

footer a:hover {
    color: #77bbff;
}
```

### Notification area styling for the messages

Last thing we need to do to have a minimalistic but user-friendly style for our app, is notifications. Firstly we style the `section .messages`, then `.message` notification block itself, and then define `background-color`s of each `.message-` tag (`-debug`/`-info`/`-success`/`-warning`/`-error`).

```CSS
section.messages {
    padding: 0;
    margin: 0;
}

.message {
    padding: 0.5rem;
    margin: 0;
    border-bottom: 1px solid #888888;
}

.message-debug {
    background-color: #aaaaaa;
}

.nessage-info {
    background-color: #99ccff;
}

.message-success {
    background-color: #ccff99;
}

.message-warning {
    background-color: #ffcc99;
}

.message-error {
    background-color: #ffaaaa;
}
```

## Conclusion

We have created a basic minimalist style for our app. We will expand on the style when adding additional user interface elements. For now, it is OK.

## Assignment

Style the base template of your blog app. You can experiment with the grid as well. Try things out.
