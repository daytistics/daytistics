from django.db import transaction
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_http_methods
from django.utils.translation import gettext_lazy as _

from app.activities.models import Activity


@login_required
def get_activities_dashboard(request):
    """
    View for the activities list. It renders the activities/dashboard.html template.

    Args:
        request (HttpRequest): The request object

    Returns:
        HttpResponse: The response object
    """
    activities = request.user.all_activities
    return render(request, "activities/dashboard.html", context={
        "activities": activities
    })


@require_POST
@login_required
def create_new_activity(request: HttpRequest):
    """
    View for creating a new activity.

    Args:
        request (HttpRequest): The request object

    Returns:
        HttpResponse: The response object
    """
    activity_name = request.POST.get("name")

    if not activity_name:
        return HttpResponse("<p class='text-red-500'>Invalid activity name</p>", status=400)

    existing_activities = Activity.objects.filter(name=activity_name)

    if not existing_activities.exists():
        with transaction.atomic():
            activity = Activity(name=activity_name)
            activity.save()
            activity.users.add(request.user)

            result_text = "Activity created successfully"
    else:
        activity = existing_activities.first()
        activity.users.add(request.user)

        result_text = "Activity updated successfully"

    return HttpResponse(
        f"<p class='text-green-500'>{_(result_text)}</p>",
        status=201,
    )


@require_http_methods(["PUT"])
@login_required
def edit_activity(request: HttpRequest, activity_id) -> HttpResponse:

    return HttpResponse("", status=204)


@require_http_methods(["DELETE"])
@login_required
def delete_activity(request: HttpRequest, activity_id) -> HttpResponse:

    return HttpResponse("", status=204)
