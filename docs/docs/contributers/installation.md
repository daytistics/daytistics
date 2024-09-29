# Installation

This tutorial covers installing the development environment to contribute to the project. Please note that [Git](https://git-scm.com/), [Python](https://www.python.org/downloads/), [Poetry](https://python-poetry.org/docs/#installation) and [Node.js](https://nodejs.org/en/download/package-manager) are required for installation.

## Clone the Repository

```
git clone git@github.com:daytistics/daytistics.git
```

## Navigate to the Project Directory

```
cd daytistics/daytistics
```

## Installing the Dependencies

```
poetry install
```

## Copying artifacts

To copy the .env-preset run

```
cp ../artifacts/.env .
```

## Enabling the Poetry Environment

```
poetry shell
```

## Installing Tailwind

```
python manage.py tailwind install
```

## Migrating the Database

```
python manage.py migrate
```

## Starting the Server

```
python manage.py runserver
```

Then switch to another terminal window and run

```
python manage.py tailwind start
```

## Tips and Tricks

### Running the Tests

```
pytest -rP
```

### npm on Windows

Tailwind is not working on Windows? Check out this [StackOverflow Discussion](https://stackoverflow.com/questions/72033027/i-am-making-a-website-using-django-and-tailwind-css-but-in-cpanel-i-am-getting).
