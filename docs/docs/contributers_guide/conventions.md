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

### Declarative Functions vs Arrow Function


### Order in Vue's Composition API

```vue
<script lang="ts" setup>
// Imports
// Props
// Emits
// Reactive data & functions using reactive data (grouped by element)
// Non-reactive data & functions (grouped by element)
// Watch functions 
// Lifecycle hooks
</script>
```

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

## API-Design

1. **Resource Naming**: Use **plural nouns** (e.g., `/users`, `/orders`).
2. **Status Codes**: Use standard codes like `200` (OK), `201` (Created), `400` (Bad Request), `404` (Not Found), `500` (Server Error).
3. **JSON Structure**: Use **camelCase** for keys, and ensure consistent and clear data structures.
4. **Error Handling**: Return structured error responses with a `message` and an optional `location`, where the error occured.
5. **Security**: Use **HTTPS**, and support **JWT** for authentication.

**Success Example**:

```json
{
  "id": 1,
  "username": "leo",
  "email": "leo@example.com",
  "links": {
    "self": "/v1/users/1"
  }
}
```

**Error Example**:

```json
{
  "detail": "Invalid username",
  "location": "app.users.models.RegisterUserView"
}
```

Adhering to these conventions ensures a consistent, clean, and maintainable codebase for everyone contributing to Daytistics.
