# Contributers Guide

Thank you for your interest in contributing to Daytistics! This section provides informations, guidelines and tips for submitting bug reports, feature suggestions, and code changes.

The easiest way to get started is by asking for help in our [Discord](https://discord.gg/xDgK5QTKJj) community.

## How to Contribute

There are several ways you can contribute to Daytistics:

- **Reporting Bugs**:
  If you encounter a bug, first search the issues for existing reports.
  If no similar issue exists, open a new one.
  Provide a clear description of the bug, including steps to reproduce it if possible.
  Screenshots, logs, or code snippets can also be very helpful.
- **Suggesting Features**:
  If you have an idea to improve Daytistics, share it by opening an issue on the issue tracker.
  Describe the proposed feature in detail, including its benefits and any potential implementation considerations.
- **Submitting Pull Requests**:
  If you want to contribute code, start by forking the Daytistics repository on GitHub.
  Follow the instructions on [this page](./install.md) to setup your local development environment.
  Make your changes on your local fork and then create a pull request to the main repository.
  Ensure your code follows our [project structure](#project-structure) and [conventions](./conventions.md).

We encourage you to comment on existing issues and pull requests to share your thoughts and feedback.
Feel free to ask questions in the issue or reach out to the project maintainers if you need assistance.
Before submitting a large contribution, consider opening an issue, starting a discussion, or talking with us on Discord to discuss your approach.

## Project Structure

Daytistics is special compared to other modern web applications. Today, most web applications are [single-page applications](https://hygraph.com/blog/difference-spa-ssg-ssr#what-is-a-single-page-application-spa) and use microservices. We are old-school because we take a monolithic approach and don't use SPAs Instead, we leverage the incredible power and flexibility of Django and mini-frameworks like Alpine.js and HTMX. We are also big fans of working quickly and efficiently in a programming language and its ecosystem.

### Applications

Like any Django application, our project is broken down into different apps and subapps. Each of these applications has its own documentation page, which is why they are only briefly listed here.

#### Config

Config is the default application of a new Django project (`django-admin startproject config`). It contains the applications settings, wsgi, asgi and the main router.

#### Core

The core app is responsible for creating and collecting information about the user's day, which is later analyzed and visualized and on which the AI ​​models are trained.

- **Daytistics**: Responsible for a Daytistics CRUD-lifecycle
- **Wellbeing**: Responsible for creating the predefined well-beings
- **Activities**: Responsible for an activities CRUD-lifecycle
- **Diaries**: Responsible for diary entries

#### Plots

The plots app is responsible for plotting relationships between the user's well-being and his activities.

#### Models

The Models app is used to train the AI ​​models on the information about the user's day.

- **Predictor**: Predicts hypothetical days
- **Suggestor**: Gives you tips based on the past

#### Account

Extends the Django User Model and overrides Django-Allauth functions.

#### Tools

Contains various cool tools and utils to make the development easier.
