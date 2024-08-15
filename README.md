# Daytistics

<p>Daytistics is a web application whose goal is to increase your productivity and incorporate good habits into your life.</p>

## Disclaimer
Daytistics-Core and all other products of the Daytistics project are in an early stage of development. We strongly recommend not to use them in production yet. Official releases will be announced [here](https://github.com/daytistics/daytistics-core/releases) in the future.



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
   git clone git@github.com:adf-web/daytistics-core.git && cd daytistics-core
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
5. **Start the tailwind watcher:**
   ```
   poetry run python manage.py tailwind start
   ```
6. **Start the development server:**
   ```
   poetry run python manage.py runserver
   ```
7. **Run the tests:**
   ```
   poetry run pytest
   ```

## License

This project is licensed under the [MIT License](./LICENSE).
