# Multilingual Configuration

Django project can bet set up and used in multilingual configuration. There are many ways to set or change language of the site interactively.

## Objectives

* Configure internationalization and localization options for the Django project - setting languages, locale, time zone, etc.
* Configure browser language detection and language setting storage in either session, cookie or URL.
* Create a language picker in `base.html` file header section.

## Internationalization and localization settings

We can enable multiple languages in the project by setting `LANGUAGES` list, which contains tuples of language code and name. For example, under `LANGUAGE_CODE` in project's `settings.py` file we add:

```Python
LANGUAGE_CODE = 'en-us'
LANGUAGES = [
    (LANGUAGE_CODE, 'English'),
    ('lt', 'Lietuvių'),
]
```

Then we can set the time zone, for example, to Lithuanian including daylight saving time when applicable. Just change `UTC` to `Europe/Vilnius`. Time zones are compatible with `ZoneInfo` module, taken from `tzdata` pip package.

```Python
TIME_ZONE = 'Europe/Vilnius'
```

Next two parameters can turn off multilingual ant time zone functionality for the project. We better leave them set to True.

```Python
USE_I18N = True
USE_TZ = True
```

Then, we scroll up to `MIDDLEWARE` parameter, and add `django.middleware.locale.LocaleMiddleware` right after `common.CommonMiddleware`. This ensures language browser detection and language setting storage in session. Locale middleware must be loaded as early as possible in case other middlewares (like user authentication) might want to take it into account, but it requires common middleware loaded already.

```Python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

Congratulations, the Django project is now working in your timezone and is configured for multilingual operations. But what if browser did not set user's prefered language? We can build a language switcher and allow users to manually change the language.

## Language picker

First we need language changeview urls functioning. Let's include `django.conf.urls.i18n` as `i18n/` path into `urlpatterns` of project's `urls.py` file:

```Python
urlpatterns = [
    path('', include('tasks.urls')),    
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
]
```

Now we can create a language picker form inside our `base.html` header section, which will call `set_language` view from `i18n`.

We need to load `i18n` tags and put `get_current_language` and `get_available_languages` into corresponding parameters: `LANGUAGE_CODE` and `LANGUAGES` list.

```HTML
<!DOCTYPE html>{% load static i18n %}{% get_current_language as LANGUAGE_CODE %}{% get_available_languages as LANGUAGES %}
<html lang="{{ LANGUAGE_CODE }}">
```

And we have set `<html lang>` argument to `LANGUAGE_CODE`, so broser (and search engines) will recognize the page as in the declared language.

Now let's add the langauge picker form in the `<header>` section:

```HTML
<header>
    ...
    <span class="spacer"></span>
    <form action="{% url 'set_language' %}" method="post">
        {% csrf_token %}
        <input type="hidden" name="next" value="{{ redirect_to }}">
        <select class="language" name="language" onchange="this.form.submit();">
            {% for lang in LANGUAGES %}
                <option value="{{ lang.0 }}" {% if lang.0 == LANGUAGE_CODE %}selected{% endif %}>
                    {{ lang.1 }}
                </option>
            {% endfor %}
        </select>
    </form>
</header>
```

* First we set the form to send it's contents to `set_language` URL by HTTP POST method. 
* We also utilize mandatory Django anti-forge form security feature so called CSRF, by including it's token.  
* We can also leave the redirect control feature in the template, by allowing the inheritable template views to set `redirect_to` variable.
* Then we just unload the languages list into HTML `<select>` tag, and in case it's value is changed by the user, we force form submission. 
* Here `lang` is the tuple from the `LANGUAGES` list defined in `settings.py` of the project, of which 0th element is language code, and 1st is verbose language name.

And in `static/css/style.css` we can define `.spacer` class with parameter `flex-grow: 1`, so our language picker would be put to the rightmost side of the page, and put some margin around the form itself.

```CSS
.spacer {
    flex-grow: 1;
}
header form {
    margin: 0.5rem;
}
```

Let's test it.

## Assignment

Configure multilingual settings for your blog project and integrate the language picker into the template. Try to put it into the footer instead this time.
