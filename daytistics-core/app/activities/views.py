from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils.translation import gettext_lazy as _

from app.activities.models import Activity


@login_required
def get_activities_list(request):
    """
    View for the activities list. It renders the activities/dashboard.html template.

    Args:
        request (HttpRequest): The request object

    Returns:
        HttpResponse: The response object
    """
    activities = Activity.objects.all()
    return render(request, "activities/dashboard.html", context={
        "activities": activities
    })


@require_POST
@login_required
def create_new_activity(request: HttpRequest):
    """
    View for creating a new activity. It renders the activities/new_activity.html template.

    Args:
        request (HttpRequest): The request object

    Returns:
        HttpResponse: The response object
    """
    print(request.body)
    print(request.POST.get("name"))
    return HttpResponse(
        f"<p class='text-green-500'>{_("Activity created successfully")}</p>",
        status=201,
    )