# Django Project Setup

## Objectives

* Setting up a virtual environment
* Creating your Django project
* Creating your first Django app
* Important initial configurations
* We will RUN it and see how it works as a local development environment
* Get familiar with User Management functionality in Django Administration

## Setting Up a Virtual Environment (venv)

A virtual environment isolates your Python/Django setup on a per-project basis, ensuring that each project has its own dependencies and packages.

### Creating a venv and installing Django

* Create a Github repository with Python `.gitignore` template, a LICENSE of your choice and clone it with VS Code into your home directory while connected to WSL.
* Run `python3 -m venv venv` in your VS Code terminal to create a virtual environment named venv. If that fails with errors, then first run `sudo apt-get install python3-venv` and retry. 
* Run `source venv/bin/activate` to activate your virtual environment.
* We can now install Django: `pip install django`.
* For later user, we should create a requirements file. Just run `pip freeze >requirements.txt`.

## Creating Your Django Project

Naming the project properly is the most important part of the project. Project name should represent the final product or even branded service the project is aimed to provide. App names usually are more generic and abstract, while project names should be more specific and entity oriented.

To create a project named `tasker`, run `django-admin startproject tasker`. You will see project's `manage.py` file created, along with project's directory with `settings.py`, `urls.py` and deployment related `asgi.py`/`wsgi.py` files. `__init__.py` is intentionally empty and will be created in every directory under `manage.py`.

Project `tasker` will grow with the material and most of the code will mutate. To keep the example code relevant temporally, we have divided the example code by suffixing it with the material number from which it is valid. For example, `tasker_01` is valid example until `tasker_04`, which takes over from the `04_` material. If you try to replicate the process, it is best that you just stick to `tasker` as project name.

### Github Django Project best practices - correct configuration by using `local_settings.py`

Sensitive configuration data, such as database passwords, email login credentials, API keys, and especially `SECRET_KEY`, should never enter Github repository. For that, we will setup .gitignored files `local_settings.py`, where we will set all the sensitive parameters. At the end of `settings.py` file we will add the following lines:

```Python
try:
    from .local_settings import *
except ImportError:
    pass
```

In that way, whatever settings we will have in our `local_settings.py` file, during Django project startup, will take over any default settings left on the `settings.py` file, which we can leave even default safely as a fallback.

### Executing Django Management Commands

Once Django project is set up, in the project's root directory you can find `manage.py` file. It is used as one of the administrative user interface to the Django project. You can pass commands with arguments to `manage.py` file when running it. For example, we will run a python shell in Django project's environment and generate a secret key to be used in `local_settings.py` of your project.

### Generating a secure `SECRET_KEY`

Make sure that in terminal you are in your Django project directory and your virtual environment is activated. Then run Django shell:

```bash
cd tasker
python manage.py shell
```

It will open an interactyve __python__ shell, so you can run python code within Django project environment. Let's import Django management utils and generate ourselves a new secret key.

```Python
from django.core.management import utils
utils.get_random_secret_key()
```

You can re-run the funcion repeatedly until the generated key "fits your taste". Then use `exit()` function or press CTRL+Z to exit the python shell.

Copy the value into your new `local_settings.py` file, as a value assignment for the SECRET_KEY constant. Example:
```Python
SECRET_KEY='5t7$Go0dCod3Ac@demy!o93e9dtd%qx!pq052h3xld=@*kpkv='
```

### Finishing Django setup by running migrations

Migrations are Django way of propagating it's apps models into database schema. Later during the development process, migrations will also be used to maintain database schema integrity relative to changes of models. It is not yet the perfect solution, since data loss is not always mitigatet. However, Django migrations so far is the best solution on the market.

You should also be able to directly execute `manage.py` file, without directly invoking python, in Linux/Mac or WSL environment.

```Bash
./manage.py migrate
```

### Run and test the local development server

Let's check out if it all works.

```Bash
./manage.py runserver
```

You can CTRL+Click the link from the terminal to open the browser, or just copy-paste it. You should see a green rocket lifting off.

## Managing Users, Groups and Permissions with built-in Django Administration functionality

We cannot log in to Django Administration before we have at least one superuser. We can create it via `manage.py`:

```Bash
./manage.py createsuperuser
```

You will be prompted for username, email and password. While username is mandatory, email is optional but it is recommended to fill in your email to be able to use password recovery functionality. 

Note, that there will be no visual indication of password entry, since for security reasons it must be entered blindly.

Also, you can use second terminal to keep `runserver` active while performing management commands.

### Accessing Admin Interface

Visit http://localhost:8000/admin/ and log in with your superuser account. You will see only `Authentication and Authorization` app for now, where you will be able to manage Users and Groups. Try editing your user and adding more data to your profile, like your full name. You can also create more users for testing.

Note: `is_superuser` gives access to Django Administration and grants all permissions, while `is_staff` only gives access to Django Administration but grants no specific Groups or Permissions. Those you can set up yourself.

## Assignment

Your project - simple blog with social network functinality. Think of a name. Avoid "blog" or "mysite" or similar generic names. 

* start a public Github repository (don't forget `.gitignore` template and LICENSE); 
* `clone` the project into an empty VS Code workspace; 
* set up Python virtual environment and activate it;
* install Django with pip;
* freeze requirements;
* initiate a Django project;
* `commit` and `push`. 

Also note, that database, since it is considered user data and not code, should never enter Github codebase. 

Replicate all the steps including user management actions to get familiar with the process.
