# About The Project

Daytistics is a web application written primarily in Python where you can enter how you spent your day. Daytistics visualizes this data and based on it gives you useful tips to increase your productivity. Additionally, we offer a self-hosted AI to predict your well-being on a hypothetical day.

> [!IMPORTANT]
> Daytistics is currently under heavy development.

## Key Features

- **Activity Tracker**: Track your activities by time
- **Well-Being Tracker**: Keep an eye on your well-being
- **Digital Diary**: Create short diary entries
- **Visualization**: Visualize connections between your well-being and your activities
- **Receive Suggestions**: Learn how to make your day more productive
- **Self-hosted AI**: Prevent unproductive days before they occur

You can find a full list of our features in the [documentation](http://docs.daytistics.com/)

## Project setting up

- Ensure Poetry is Properly Installed [Poetry Official Documentation](https://python-poetry.org/docs/#installing-with-the-official-installer)
- Navigate to the Project Directory: `cd my-project`
- If you have a pyproject.toml file with dependencies listed, you can install them by running: `poetry install`
- Fill `.env` file with environment variables values for: DJANGO_SECRET_KEY, DJANGO_ALLOWED_HOSTS, DEFAULT_ACTIVITIES
- **(Windows only)** For npm support under the Python we should define path to npm in environment variable: NPM_BIN_PATH
[StackOverflow Discussion](https://stackoverflow.com/questions/72033027/i-am-making-a-website-using-django-and-tailwind-css-but-in-cpanel-i-am-getting)
- Poetry automatically creates a virtual environment for your project. To activate it, run: `poetry shell`
- Install all required packages for tailwind support: `python manage.py tailwind install`
- Make sure that you prepared static with tailwind: `python manage.py tailwind start`
- Apply existing migrations on the project: `python manage.py migrate`
- With the virtual environment activated, you can run your project scripts or start development: `python manage.py runserver`

## Contributing

Contributions are welcome! If you want to contribute to the project you can take a look into [CONTRIBUTING.md](./CONTRIBUTING.md). There you can find guidelines and useful tips to get started.

If you are not a programmer, you can still contribute financially. Financial contributions help me prioritize work on this project over others and show me that there is a real need for project development.

### Thanks to

- [@DavydIkkes](https://www.linkedin.com/in/davyd-ikkes-19581b316/)
- [@MrHoffnung](https://hopeware.de)

## Communication

Consider joining our [discord](https://discord.gg/GTV7XnPb) to stay up-to-date on events, updates, and connect with other members.

## License

This project is licensed under the [MIT License](./LICENSE).
