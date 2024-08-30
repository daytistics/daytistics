# Installation and Deployment

## Prerequisites

- **Python 3.x**: [Download Python](https://www.python.org/downloads/)
- **Poetry**: [Download Poetry](https://python-poetry.org/)
- **Docker**: [Download Docker](https://www.docker.com/)
- **Git**: [Download Git](https://git-scm.com/downloads)

## Development Installation

### Daytistics-Core
Required steps for project start up:
- Navigate to the Project Directory: `cd daytistics/daytistics-core`
- Install the dependencies by running `poetry install`
- Fill `.env` file with environment variables values for: DJANGO_SECRET_KEY, DJANGO_ALLOWED_HOSTS
- **(Windows only)** For npm support under the Python we should define path to npm in environment variable: NPM_BIN_PATH
[StackOverflow Discussion](https://stackoverflow.com/questions/72033027/i-am-making-a-website-using-django-and-tailwind-css-but-in-cpanel-i-am-getting)
- Poetry automatically creates a virtual environment for your project. To activate it, run: `poetry shell`
- Install all required packages for tailwind support: `python manage.py tailwind install`
- Make sure that you prepared static with tailwind: `python manage.py tailwind start`
- Apply existing migrations on the project: `python manage.py migrate`
- With the virtual environment activated, you can run your project scripts or start development: `python manage.py runserver`

## Local Deployment

To be continued...

## How to connect the core with the model?

To be continued...
