# Project Structure

Daytistics is split into multiple web services, which work together to ensure a good user experience and performance. It all services we don't use [SPA](https://hygraph.com/blog/difference-spa-ssg-ssr#what-is-a-single-page-application-spa) frameworks like Vue or React. Instead we use the [SSR](https://hygraph.com/blog/difference-spa-ssg-ssr#what-is-server-side-rendering-ssr) features of Django.

## Sample Project Structure

```
my-app/
├── src/
│   ├── app1/
│   │   ├── migrations/
│   │   │   ├── migration1.py
│   │   │   └── migration2.py
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   └── views.py
│   └── config/
│       ├── settings/
│       │   ├── base.py
│       │   ├── constants.py
│       │   ├── dev.py
│       │   └── prod.py
│       ├── __init__.py
│       ├── asgi.py
│       ├── urls.py
│       └── wsgi.py
├── static/
│   ├── css/
│   │   └── style.css
│   ├── icons/
│   │   ├── cross.svg
│   │   └── door.svg
│   ├── images/
│   │   ├── logo.png
│   │   └── rabbit.jpg
│   └── js/
│       └── hello_world.js
├── templates/
│   ├── app1/
│   │   ├── includes/
│   │   │   └── hero.html
│   │   ├── home.html
│   │   └── imprint.html
│   ├── includes/
│   │   ├── _sidebar.html
│   │   └── _navbar.html
│   ├── 404.html
│   ├── base.html
│   └── locale/
│       └── de/
│           └── LC_MESSAGES/
│               ├── django.mo
│               └── django.po
├── tests/
│   ├── app1/
│   │   ├── test_app1_views.py
│   │   └── test_app1_models.py
│   ├── conftest.py
│   ├── factories.py
│   ├── settings.py
│   └── test_fixtures.py
├── .dockerignore
├── .env
├── db.sqlite3
├── Dockerfile
├── manage.py
├── poetry.lock
└── pyproject.toml
```

## Daytistics-Core

Core of the application which is hosted by us on [daytistics.com](https://daytistics.com). It manages the creation, editing and deletion of daytistics, activities, feelings and diary entries and takes care of user management.

### Applications

- **Account**: User management and overriding the Django built in user
- **Activities**: Activity type management
- **Config**: Django configuration
- **Daytistics**: Daytistics management
- **Home**: "Static" homepage sites
- **Tools**: Various practical tools

## Daytistics-Model

To be continued...
