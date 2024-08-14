# Daytistics

![Logo](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/th5xamgrr6se0x5ro4g6.png)

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

## Contributing

Contributions are welcome! If you want to contribute to the project you can take a look into [CONTRIBUTING.md](./CONTRIBUTING.md). There you can find guidelines and useful tips to get started.

### Thanks to
😭 No contributers yet...

## Installation

### Pre-Requirements
- **Python (v3.12)**: <a href="https://www.debugpoint.com/install-python-3-12-ubuntu/">Installation Guide</a>
- **Poetry (v1.8.2)**: <a href="https://python-poetry.org/docs/">Installation Guide</a>
- **Node.js (v20.16.0)**: <a href="https://nodejs.org/en/download/package-manager">Installation Guide</a>

1. **Clone the repository:**
    ```
    git clone git@github.com:adf-tech/daytistics-web.git && cd daytistics-web
    ```

2. **Install the required dependencies:**
    ```
    poetry install
    ```
3. **Install Tailwind CSS:**
   ```
   poetry run python manage.py tailwind install
   ```
4. **Run database migrations:**
    ```
    poetry run python manage.py makemigrations && poetry run python manage.py migrate
    ```
6. **Start the tailwind watcher:**
    ```
    poetry run python manage.py tailwind start
    ```
6. **Start the development server:**
    ```
    poetry run python manage.py runserver
    ```

## Running Tests

To run tests, run the following command

```bash
  poetry run pytest
```

## License

This project is licensed under the [MIT License](./LICENSE).
