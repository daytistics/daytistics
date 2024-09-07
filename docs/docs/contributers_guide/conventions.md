# Conventions

This document outlines the conventions used in this project. Following these conventions helps ensure consistency and maintainability across the codebase.

## Code Styling

### General Principles

- **[SOLID Principles](https://medium.com/@umaparvat/solid-principles-in-python-c9c3c337e0e1)**: The five golden rules of OOP
- **[DRY](https://docs.getdbt.com/terms/dry#why-write-dry-code)**: "Don't repeat yourself!"

### Language-Specific Guidelines

- **Python**: Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide.
- **JavaScript**: Adhere to the [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript).
- **Django**: Stick to the [Django Coding Style](https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/coding-style/).

### Naming Conventions

- **Variables**: Use `snake_case` for Python and `camelCase` for JavaScript.
- **Functions/Methods**: Use `snake_case` for Python and `camelCase` for JavaScript.
- **Classes**: Use `PascalCase` for all languages.
- **Constants**: Use `UPPER_SNAKE_CASE` for constants.

### Indentation

- Use **4 spaces** per indentation level in Python.
- Use **2 spaces** per indentation level in JavaScript.

## Commit Messages

- **Format**: Use the following format for commit messages: <br>
  `type: short description`
  <br><br>
- **Types**: Use these types for commits:
  - `feat`: A new feature
  - `fix`: A bug fix
  - `docs`: Documentation changes
  - `style`: Code style changes (formatting, missing semi-colons, etc.)
  - `refactor`: Code refactoring without adding features or fixing bugs
  - `test`: Adding or updating tests
  - `chore`: Maintenance tasks like build process, package management, etc.

## File and Directory Structure

- **Source Code**: Place all source code files in the `app/` directory. You can find more information on [this page](./overview.md) file.
- **Tests**: Place test files in the `tests/` directory, mirroring the structure of the `app/` directory.
- **Configuration**: Keep configuration files (e.g., .env) in the root directory.

## Documentation

- **Docstrings**: Use [Google Style](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings) docstrings in Python.
- **Inline Comments**: Use inline comments sparingly and only when the code isn't self-explanatory.

## Testing

- **Unit Tests**: Write unit tests for all new features and bug fixes.
- **Test Naming**: Name test files and functions descriptively, using `test_` as a prefix for functions.

## Translation

Please make sure that you add all translatable strings to the corresponding files (currently only `locale/de/LC_MESSAGES/django.po`). If you cannot translate the messages yourself, please create a new issue with the tag `translation` after merging your pull request, in which you explain which snippets need to be translated.

### Conventions

Please follow the following conventions to secure readability and maintainability:

- **Write in the appropriate section**: Sections are marked by the `# SECTION` comment.
  - `SENTENCES_STD`: This section includes standard sentences used across the application, such as common phrases or dialogue.
  - `SHORTS_STD`: This section contains short, standard texts like labels and buttons (max 3 words).
  - `BODY_TEXT_STD`: This section holds longer blocks of standard text, such as paragraphs or descriptions.
  - `ERROR_STD`: This section includes standard error messages that are used throughout the application.
  - `SENTENCES_FORMAT`: This section is for sentences with specific formatting or placeholders.
  - `SHORTS_FORMAT`: This section contains short texts with formatting or placeholders.
  - `BODY_TEXT_FORMAT`: This section includes longer blocks of text with formatting or placeholders.
  - `ERROR_FORMAT`: This section contains error messages that include formatting or placeholders.
- **Use reference comments**: to explain relations with the source code
- **Use the fuzzy flag**: For values that don't have to be translated (yet)
- **Add context**: for non-self-explanatory values
- **Snippet order**: Alphabetically

Adhering to these conventions ensures a consistent, clean, and maintainable codebase for everyone contributing to Daytistics.
