---
sidebar_position: 2
---

# Environment Setup

This guide will help you to set up your development environment for the Daytistics project. We will guide you through the installation of the necessary tools and show you how to set up the project on your local machine.

## Prerequisites

Before you start setting up your development environment, make sure you have the following tools installed on your machine:

* [Python](https://www.python.org/downloads/)
* [Node.js](https://nodejs.org/en/download/)
* [Docker](https://www.docker.com/get-started)
* [Docker Compose](https://docs.docker.com/compose/install/)
* [Git](https://git-scm.com/downloads)

## Installation

### Clone the Repository

The first step is to clone the Daytistics repository to your local machine. Open a terminal and run the following command:

```sh
git clone 
```

### Running with Docker

Thanks to Docker and Docker Compose, setting up Daytistics is easy. Navigate to the root directory of the project and run the following command:

```sh
docker-compose -f docker-compose.dev.yml up --build
```

The following services will be started:

* **Backend (port 8000)**: The FastAPI backend of the Daytistics project.
* **Frontend (port 3000)**: The Nuxt.js frontend of the Daytistics project.
* **Database (port 5432)**: The PostgreSQL database of the Daytistics project.
* **Documentation (port 4000)**: The Docusaurus documentation of the Daytistics project.

## Other Commands

:::tip

You can check the container ID by running `docker ps` and looking for the container with the name `daytistics-<service-name>` image.

:::

### Running Tests

```sh
# Run backend tests (unit/integration tests)
docker exec -it <container-id> uv run pytest 
```

```sh	
# Run frontend tests (unit/integration tests)
docker exec -it <container-id> pnpm run test:unit
```

```sh
# Run frontend e2e tests
docker exec -it <container-id> pnpm run test:e2e
```

### Linting

```sh
# Lint backend code
docker exec -it <container-id> uv run ruff check
```

```sh
# Lint frontend code
docker exec -it <container-id> pnpm run lint
```

### Formatting

```sh
# Format backend code
docker exec -it <container-id> uv run ruff format
```

```sh
# Format frontend code
docker exec -it <container-id> pnpm run format
```

## Database 

:::warning

Do not migrate the database unless you have confirmation from the maintainers. 

:::

### Generate Migrations

```sh
docker exec -it <container-id> uv run alembic revision --autogenerate -m "<message>"
```

### Apply Migrations

```sh
docker exec -it <container-id> uv run alembic upgrade head
```

## Dev Containers

We recommend using the Visual Studio Code Remote - Containers extension to develop Daytistics. This extension allows you to open the project in a Docker container with all the necessary tools and dependencies pre-installed.

To use the Dev Container, download VS-Code and install the Remote - Containers extension. Open VS-Code and press `F1` to open the command palette. Search for `Dev Containers: Open Folder in Container` and select the root directory of the Daytistics project.
