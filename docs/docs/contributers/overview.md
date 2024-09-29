# Hello, Contributor!

Thank you for your interest in contributing to Daytistics! This section provides informations, guidelines and tips for submitting bug reports, feature suggestions, and code changes.

The easiest way to get started is by asking for help in our [Discord](https://discord.gg/xDgK5QTKJj) community.

## Code Base

Our codebase is split into three services: the backend/core, the frontend and the AI modeler. Each service is responsible for a specific part of the application and communicates with the others through RESTful APIs.

The core and the AI modeler are written in Python using the Django framework and Django-Ninja for the API. We use Django because of its robustness, scalability, and security features. Another benefit is it's large community and ecosystem of plugins and libraries.

The frontend is written in TypeScript using Nuxt, a meta-framework built on top of Vue. Nuxt provides a powerful and flexible frontend framework that allows us to build a fast, responsive, and user-friendly interface. The design of our frontend is based on Tailwind CSS, a utility-first CSS framework that helps us create a consistent and visually appealing UI, and Flowbite, a Tailwind CSS and JavaScript UI kit and component library.

In the future we might use Zig and Web-Assembly for performance-critical parts of the application. Zig is a modern, high-performance systems programming language that compiles to machine code. It is designed for safety, speed, and simplicity, making it an excellent choice for performance-critical code.

Each component is modular and follows best practices to ensure maintainability and scalability. We encourage contributors to familiarize themselves with the structure and conventions used in our codebase.


## Structure

If you want to learn about the structure of a specific service, check out the corresponding page in the services section. Each page provides an overview of the service, its purpose, and how it interacts with other services.

Learn more about the [core](./services/core/overview.md), [frontend](./services/frontend/overview.md), and [AI modeler](./services/modeler/overview.md).