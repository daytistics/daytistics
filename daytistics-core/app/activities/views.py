from django.shortcuts import render


def get_activities_list(request):
    """
    View for the activities list. It renders the activities/dashboard.html template.

    Args:
        request (HttpRequest): The request object

    Returns:
        HttpResponse: The response object
    """
    return render(request, "activities/dashboard.html")


def create_new_activity(request):
    """
    View for creating a new activity. It renders the activities/new_activity.html template.

    Args:
        request (HttpRequest): The request object

    Returns:
        HttpResponse: The response object
    """
    return render(request, "activities/new_activity.html")