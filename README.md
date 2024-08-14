# Daytistics

Daytistics is a web application whose goal is to increase your productivity and incorporate good habits into your life. 

## Technologies

<p align="left">
  <img src="https://raw.githubusercontent.com/devicons/devicon/6910f0503efdd315c8f9b858234310c06e04d9c0/icons/django/django-plain.svg" width="50px" alt="Django" title="Django">
  <img width="15px">
  <img src="https://raw.githubusercontent.com/devicons/devicon/6910f0503efdd315c8f9b858234310c06e04d9c0/icons/alpinejs/alpinejs-original.svg" width="50px" alt="AlpineJS" title="AlpineJS">
  <img width="15px">
  <img src="https://i.imgur.com/uHQ2pvy.png" width="50px" alt="HTMX" title="HTMX">
  <img width="15px">
  <img src="https://raw.githubusercontent.com/devicons/devicon/6910f0503efdd315c8f9b858234310c06e04d9c0/icons/tailwindcss/tailwindcss-original.svg" width="50px" alt="TailwindCSS" title="TailwindCSS">
  <img width="15px">
  <img src="https://raw.githubusercontent.com/devicons/devicon/6910f0503efdd315c8f9b858234310c06e04d9c0/icons/postgresql/postgresql-original.svg" width="50px" alt="PostgreSQL" title="PostgreSQL">
  <img width="15px">
</p>

## Installation

### Pre-Requirements
- **Python**: <a href="https://www.debugpoint.com/install-python-3-12-ubuntu/">Installation Guide</a>
- **Poetry**: Installation Guide
- 

1. Clone the repository:
    ```
    git clone git@github.com:adf-tech/daytistics-web.git && cd daytistics-web
    ```

2. Install the required dependencies:
    ```
    poetry install
    ```
3. Install Tailwind CSS:
   ```
   poetry run python manage.py tailwind install
   ```
4. Run database migrations:
    ```
    poetry run python manage.py makemigrations
    ```
    ```
    poetry run python manage.py migrate
    ```
6. Start the tailwind watcher:
    ```
    poetry run python manage.py tailwind start
    ```
6. Start the development server:
    ```
    poetry run python manage.py runserver
    ```

## Structure
- **config**: Default Django project file with configuration files
- **main**: All about daytistic entries
- **analytics**: Analysis of entries from "main"
- **journal**: Journal functionalities
- **others**: Everything else

## Contributing

Contributions are welcome! Please follow the guidelines in [CONTRIBUTING.md](./CONTRIBUTING.md).

## License

This project is licensed under the [MIT License](./LICENSE).
