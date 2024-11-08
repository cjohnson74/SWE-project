> A batteries-included Django starter project. To learn more visit [LearnDjango.com](https://learndjango.com).


https://github.com/wsvincent/djangox/assets/766418/a73ea730-a7b4-4e53-bf51-aa68f6816d6a


## 🚀 Features

- Django 5.1 & Python 3.12
- Install via [Pip](https://pypi.org/project/pip/) or [Docker](https://www.docker.com/)
- User log in/out, sign up, password reset via [django-allauth](https://github.com/pennersr/django-allauth)
- Static files configured with [Whitenoise](http://whitenoise.evans.io/en/stable/index.html)
- Styling with [Bootstrap v5](https://getbootstrap.com/)
- Debugging with [django-debug-toolbar](https://github.com/jazzband/django-debug-toolbar)
- DRY forms with [django-crispy-forms](https://github.com/django-crispy-forms/django-crispy-forms)
- Custom 404, 500, and 403 error pages
----

## Table of Contents
* **[Installation](#installation)**
  * [Pip](#pip)
  * [.env](#env)
  * [Getting Canvas Access Token](#getting-canvas-access-token)
  * [Seed Canvas Data](#seed-canvas-data)
  * [Run Server](#run-server)
  * [Docker](#docker)
* [Next Steps](#next-steps)
* [Contributing](#contributing)
* [Support](#support)
* [License](#license)

----

## 📖 Installation
DjangoX can be installed via Pip or Docker. To start, clone the repo to your local computer and change into the proper directory.

```
$ git clone https://github.com/wsvincent/djangox.git
$ cd djangox
```

### Pip

```
$ python -m venv .venv

# Windows
$ Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
$ .venv\Scripts\Activate.ps1

# macOS
$ source .venv/bin/activate

### .env
```markdown
# Django
SECRET_KEY=<django-secret-key>
DEBUG=True

# MongoDB
DB_HOST='<mongodb-host>'
DB_PORT=<mongodb-port>
DB_NAME='<mongodb-name>'
DB_USER='<mongodb-user>'
DB_PASSWORD='<mongodb-password>'
DB_AUTH_SOURCE='<mongodb-auth-source>'

# Canvas API
CANVAS_ACCESS_TOKEN='<canvas-access-token>'
ENROLLMENT_TERM_ID=10160000000002195
```

### Getting Canvas Access Token

For testing your application before you've implemented OAuth, the simplest option is to generate an access token on your user's profile page. Note that asking any other user to manually generate a token and enter it into your application is a violation of Canvas' API Policy. Applications in use by multiple users MUST use OAuth to obtain tokens.

To manually generate a token for testing:

Click the "profile" link in the top right menu bar, or navigate to /profile
Under the "Approved Integrations" section, click the button to generate a new access token.
Once the token is generated, you cannot view it again, and you'll have to generate a new token if you forget it. Remember that access tokens are password equivalent, so keep it secret.

Source: https://canvas.instructure.com/doc/api/file.oauth.html#manual-token-generation

### Seed Canvas Data
```markdown
(.venv) djangox $ pip install -r requirements.txt
(.venv) djangox $ python seed_canvas_data.py
```

# These commands are not needed anymore as we are using MongoDB now, but we don't want to delete them
```markdown
#(.venv) djangox $ python manage.py migrate
#(.venv) djangox $ python manage.py createsuperuser
```

### Run Server  
```markdown
(.venv) djangox $ python manage.py runserver
```

### Docker

To use Docker with PostgreSQL as the database update the `DATABASES` section of `django_project/settings.py` to reflect the following:

```python
# django_project/settings.py
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": "db",  # set in docker-compose.yml
        "PORT": 5432,  # default postgres port
    }
}
```

The `INTERNAL_IPS` configuration in `django_project/settings.py` must be also be updated:

```python
# config/settings.py
# django-debug-toolbar
import socket
hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
INTERNAL_IPS = [ip[:-1] + "1" for ip in ips]
```

And then proceed to build the Docker image, run the container, and execute the standard commands within Docker.

```
$ docker compose up -d --build
$ docker compose exec web python manage.py migrate
$ docker compose exec web python manage.py createsuperuser
# Load the site at http://127.0.0.1:8000
```

## Next Steps

- Add environment variables. There are multiple packages but I personally prefer [environs](https://pypi.org/project/environs/).
- Add [gunicorn](https://pypi.org/project/gunicorn/) as the production web server.
- Update the [EMAIL_BACKEND](https://docs.djangoproject.com/en/4.0/topics/email/#module-django.core.mail) and connect with a mail provider.
- Make the [admin more secure](https://opensource.com/article/18/1/10-tips-making-django-admin-more-secure).
- `django-allauth` supports [social authentication](https://django-allauth.readthedocs.io/en/latest/providers.html) if you need that.

I cover all of these steps in tutorials and premium courses over at [LearnDjango.com](https://learndjango.com).

----

## 🤝 Contributing

Contributions, issues and feature requests are welcome! See [CONTRIBUTING.md](https://github.com/wsvincent/djangox/blob/master/CONTRIBUTING.md).

## ⭐️ Support

Give a ⭐️  if this project helped you!

## License

[The MIT License](LICENSE)
