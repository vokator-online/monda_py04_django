# Templates for default user views

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

