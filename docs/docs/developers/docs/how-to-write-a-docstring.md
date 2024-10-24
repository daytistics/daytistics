As you've probably read on the [Where are the Docs?](./where-are-the-docs.md) page or noticed while exploring our code, we do you use primarily docstrings in our code. This is a quick guide on how to write a docstring in Python and TypeScript. We'll cover how to document functions, classes and API endpoints. And we do also cover when to NOT write a docstring.

## 🛠️ Documenting Functions
### Python
```py
def add(a: int, b: int) -> int:
    """
    Add two numbers together.

    Args:
        a (int): The first number.
        b (int): The second number.

    Returns:
        int: The sum of the two numbers.
    """
    return a + b
```

As you can see, the docstring is a multi-line string that is placed directly below the function definition. It should contain a brief description of the function, followed by a list of arguments and their types, and finally the return type of the function. Please use also type hints for primitive types in your function signature.

### TypeScript
```ts
/**
 * Add two numbers together.
 * 
 * @param a The first number.
 * @param b The second number.
 * @returns The sum of the two numbers.
 */
function add(a: number, b: number): number {
    return a + b;
}
```

In TypeScript, the docstring is a single-line comment that is placed directly above the function definition. It should contain a brief description of the function, followed by a list of arguments and their types, and finally the return type of the function. Please use also type hints for primitive types in your function signature.

## 📦 Documenting Classes
### Python
```py
class Calculator:
    """
    A simple calculator class.
    """

    def __init__(self):
        pass

    def add(self, a: int, b: int) -> int:
        """
        Add two numbers together.

        Args:
            a (int): The first number.
            b (int): The second number.

        Returns:
            int: The sum of the two numbers.
        """
        return a + b
```

A class docstring should be placed directly below the class definition and should contain a brief description of the class. The docstring for each method should be placed directly below the method definition and should follow the same format as the function docstring. The `__init__` method does not need a docstring unless it does something unusual.

### TypeScript
```ts
/**
 * A simple calculator class.
 */
class Calculator {
    /**
     * Add two numbers together.
     * 
     * @param a The first number.
     * @param b The second number.
     * @returns The sum of the two numbers.
     */
    add(a: number, b: number): number {
        return a + b;
    }
}
```

A class docstring should be placed directly above the class definition and should contain a brief description of the class. The docstring for each method should be placed directly above the method definition and should follow the same format as the function docstring.

## 🚀 Documenting API Endpoints

### Python
```py
@router.post(
    "{daytistic_id}/add-activity",
    response={201: AddActivityEntryResponse, 404: Message, 422: Message},
    auth=JWTAuth(),
)
def add_activity_to_daytistic(
    request, daytistic_id: int, payload: AddActivityEntryRequest
):
    """
    POST-Endpoint to add an Activity to a Daytistic.

    This endpoint adds an Activity to a Daytistic for the current user. 
    It is protected by JWT authentication.

    **Path:**
        daytistic_id: int - The ID of the Daytistic to add the Activity to

    **Body:**
        id: int - The ID of the Activity
        start_time: int - The start time of the Activity in minutes since midnight
        end_time: int - The end time of the Activity in minutes since midnight

    **Response:**
        201: AddActivityEntryResponse - A list of all Activities in the Daytistic
        404: Message - Daytistic not found
        422: Message - Invalid start time, end time, or Activity overlaps with existing Activity
        500: Message - Internal server error
    """

    pass
```

```py
@router.get(
    "{daytistic_id}", response={200: DaytisticResponse, 404: Message}, auth=JWTAuth()
)
def get_daytistic(request, daytistic_id: int):
    """
    GET-Endpoint to retrieve a single Daytistic.

    This endpoint retrieves a single Daytistic for the current user by its ID. It is protected by JWT authentication.

    **Query:**
        daytistic_id: int - The ID of the Daytistic to retrieve

    **Response:**
        200: DaytisticResponse - The Daytistic object as JSON
        404: Message - Daytistic not found
        500: Message - Internal server error
    """

    pass
```

API endpoint docstrings should be placed directly above the endpoint definition and should contain a brief description of the endpoint, followed by a list of path parameters, query parameters, and request body parameters. The docstring should also include a list of possible responses and their meanings.

### TypeScript

We do not use TypeScript for our backend, so we do not have any examples for TypeScript API endpoint docstrings. 