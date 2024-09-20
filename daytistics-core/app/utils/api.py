from django.http import JsonResponse
import inspect
from django.conf import settings

def success_response(content: dict, status: int=200) -> JsonResponse:
    return JsonResponse(content, status=status, safe=False)

def error_response(message: str, error_code: int=400) -> JsonResponse:
    """
    Generate a JSON response with an error message and optional location information if in `DEBUG` mode.
    Args:
        message (str): The error message to be included in the response.
        error_code (int): The HTTP status code to be set in the response.
    Returns:
        JsonResponse: A JSON response object containing the error message and optional location information.
    Example:
        >>> error_response("Invalid input", 400)
        JsonResponse({'message': 'Invalid input'}, status=400)
    """

    calling_file = inspect.stack()[1]
    calling_function = calling_file.function
    calling_line = calling_file.lineno

    if settings.DEBUG:
        location = {'file': calling_file.filename, 'function': calling_function, 'line': calling_line}
        return JsonResponse({'message': message, 'location': location}, status=error_code)
    
    return JsonResponse({'message': message}, status=error_code)