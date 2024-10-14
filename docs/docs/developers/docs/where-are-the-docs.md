You've probably expected to find tons of code documentation in this section. But the truth is, that this is not necessary. Almost every function and class in this codebase is documented with docstrings. This means that you can find the documentation for a function or class by looking at the docstring of that function or class. This is why we don't provide a lot of additional documentation in this section. If you are looking for a specific function or class, you can find it by looking at the docstrings in the codebase.

## ❓ FAQ

### How to learn Django, Nuxt etc.?

#### Python

- **[DataMentor - Learn Python](https://www.datamentor.io/python)**: Short beginners guide to Python
- **[Asabeneh/30-Days-Of-Python](https://github.com/Asabeneh/30-Days-Of-Python)**: Get a deeper understanding of Python in 30 days

#### JavaScript/TypeScript

- **[Asabeneh/30-Days-Of-JavaScript](https://github.com/Asabeneh/30-Days-Of-JavaScript)**: Learn JavaScript in 30 days
- **[TypeScript in 5 minutes](https://www.typescriptlang.org/docs/handbook/typescript-in-5-minutes.html)**: Quick introduction to TypeScript

#### Django

- **[W3Schools - Django Tutorial](https://www.w3schools.com/django/)**: Django tutorial on W3Schools

#### Nuxt

- **[Traversy Media - Vue.js Crash Course 2024](https://www.youtube.com/watch?v=VeNfHj6MhgA)**: Vue.js crash course by the popular YouTuber Traversy Media
- **[Nuxt 3 Tutorial](https://www.youtube.com/playlist?list=PL4cUxeGkcC9haQlqdCQyYmL_27TesCGPC)**: YouTube playlist by Net Ninja

### Where can I find the codebases for the frontend and the backend?

If you are in the root directory of the project, you can find the frontend codebase in the `frontend` directory and the backend codebase in the `backend` directory. Please note that the real backend codebase is located in `backend/daytistics`.

### Where can I find the API endpoints?

If you a look into `backend/daytistics/core/api.py`, you will find different routers which are imported from the different apps. Each router contains the API endpoints for the app. The routers are then added to the `api` object which is the main API object of the project. If you follow the imports of the routers, you will find the API endpoints for the app. The API endpoints are configured with [Django-Ninja](https://django-ninja.dev/).

```py

from ..activities.api import router as activities_router
from ..users.api import router as users_router
from ..daytistics.api import router as daytistics_router

# [...]

api.add_router("/users/", users_router)
api.add_router("/daytistics/", daytistics_router)
api.add_router("/activities/", activities_router)
```