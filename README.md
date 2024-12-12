> A batteries-included Django starter project. To learn more visit [LearnDjango.com](https://learndjango.com).

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
* [Screenshots](#screenshots)
* [License](#license)

----

## 📖 Installation
DjangoX can be installed via Pip or Docker. To start, clone the repo to your local computer and change into the proper directory.

```
$ git clone https://github.com/cjohnson74/SWE-project.git
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

# Linux
$ source .venv/bin/activate

# Mac/Linux
$ pip install -r requirements.txt

# Windows
$ .venv\Scripts\pip.exe install -r requirements.txt
```

### System Dependencies

This project requires Poppler for PDF processing. Install it based on your operating system:

**macOS:**
```bash
brew install poppler
```

**Ubuntu/Debian:**
```bash
sudo apt-get install poppler-utils
```

**Windows:**
1. Download Poppler from: [Poppler for Windows](http://blog.alivate.com.au/poppler-windows/)
2. Extract to a folder (e.g., C:\poppler-xx)
3. Add the `bin` folder to your PATH environment variable
4. Restart your terminal/IDE

To verify the installation:
```bash
# Mac/Linux
which pdftoppm

# Windows
where pdftoppm
```

### .env
```markdown
# Django
SECRET_KEY='django-insecure-0peo@#x9jur3!h$ryje!$879xww8y1y66jx!%*#ymhg&jkozs2'

# Canvas API
CANVAS_ACCESS_TOKEN='<canvas-access-token>'
ENROLLMENT_TERM_ID=10160000000002195

# Django
DATABASE_URL='sqlite:///db.sqlite3'

# Claude API
CLAUDE_API_KEY='<claude-api-key>'
```

### Getting Canvas Access Token

For testing your application before you've implemented OAuth, the simplest option is to generate an access token on your user's profile page. Note that asking any other user to manually generate a token and enter it into your application is a violation of Canvas' API Policy. Applications in use by multiple users MUST use OAuth to obtain tokens.

To manually generate a token for testing:

1. Click the "profile" link in the top right menu bar, or navigate to /profile
2. Under the "Approved Integrations" section, click the button to generate a new access token.
3. Once the token is generated, you cannot view it again, and you'll have to generate a new token if you forget it. Remember that access tokens are password equivalent, so keep it secret.

Source: https://canvas.instructure.com/doc/api/file.oauth.html#manual-token-generation

### Claude API Key
1. Go to https://console.anthropic.com/settings/keys
2. Click on "+ Create Key"
3. Copy the API key and paste it into the `.env` file
4. Add money to your account

### Migrate and Create Superuser
```markdown
#(.venv) djangox $ python manage.py migrate
#(.venv) djangox $ python manage.py createsuperuser
```

### Seed Canvas Data
```markdown
(.venv) djangox $ python seed_canvas_data.py
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

## Screenshots
![Screenshot 2024-12-12 at 1 41 48 PM](https://github.com/user-attachments/assets/7f4204ca-5c35-411f-8ad8-bb935ff0d9c3)
![Screenshot 2024-12-12 at 1 42 28 PM](https://github.com/user-attachments/assets/8b69cc58-7590-47aa-9417-aef7a573a027)
![Screenshot 2024-12-12 at 1 43 10 PM](https://github.com/user-attachments/assets/0d3d8e46-1534-4461-b35d-a92e8f9287d8)
![Screenshot 2024-12-12 at 1 43 22 PM](https://github.com/user-attachments/assets/07e22a5e-d989-4069-be2b-75a485c6721f)
![Screenshot 2024-12-12 at 1 47 25 PM](https://github.com/user-attachments/assets/5aa3de84-0846-4d4c-a32a-66d45e88a644)
![Screenshot 2024-12-12 at 1 47 42 PM](https://github.com/user-attachments/assets/db19506d-1ff0-423f-b7ca-1e62357fdd95)
![Screenshot 2024-12-12 at 1 48 37 PM](https://github.com/user-attachments/assets/bd9663b4-d52b-40af-956c-557f23fb3944)
![Screenshot 2024-12-12 at 2 27 33 PM](https://github.com/user-attachments/assets/7a1fadcf-99c2-4bb7-a56f-3dd052c0a2c9)
![Screenshot 2024-12-12 at 2 27 40 PM](https://github.com/user-attachments/assets/21f791a7-59fd-4fbf-a4de-1d64ffd422cf)
![Screenshot 2024-12-12 at 2 28 05 PM](https://github.com/user-attachments/assets/dfc59540-6764-4dcb-9bf9-d70985ceb178)
![Screenshot 2024-12-12 at 2 28 15 PM](https://github.com/user-attachments/assets/05801077-fa66-44a3-a0ce-514849850ab0)
![Screenshot 2024-12-12 at 2 28 23 PM](https://github.com/user-attachments/assets/7a8132af-a8ac-45ad-afd8-dd74d6e08dff)
![Screenshot 2024-12-12 at 2 28 30 PM](https://github.com/user-attachments/assets/b438c6e6-ef0f-465c-8289-489b20802e4f)

## License

[The MIT License](LICENSE)
