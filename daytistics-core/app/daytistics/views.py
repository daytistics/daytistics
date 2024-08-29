# DJANGO IMPORTS
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.conf import settings
import re
import json


# PROJECT IMPORTS
from .models import Daytistic, ActivityEntry
from app.activities.models import Activity
from app.tools.decorators import internal_only


# OTHER IMPORTS
from datetime import datetime, timedelta
from django.utils.translation import gettext_lazy as _


@login_required
def dashboard(request: HttpRequest) -> HttpResponse:
    """
    View for the dashboard. It returns the daytistics list based on the list type and list size. The list size is not in use at the moment, but it will be used maybe in the future.

    Args:
        request (HttpRequest): The request object

    Returns:
        HttpResponse: The response object
    """
    list_type = request.GET.get("listType")

    try:
        list_size = int(request.GET.get("listSize"))
    except TypeError:
        list_size = int(settings.DEFAULT_DAYTISTICS_NUMBER_IN_DASHBOARD)

    user = request.user
    context = dict()

    context["daytistics_list_limit"] = settings.DEFAULT_DAYTISTICS_NUMBER_IN_DASHBOARD

    match list_type:
        case "random":
            try:
                context["daytistics_list"] = user.get_daytistics_randomized(list_size)
            except ValueError:
                context["daytistics_list"] = user.get_daytistics_randomized(
                    settings.DEFAULT_DAYTISTICS_NUMBER_IN_DASHBOARD
                )

        case "updatedAt":
            try:
                context["daytistics_list"] = user.get_daytistics_by_time_updated(
                    list_size
                )
            except ValueError:
                context["daytistics_list"] = user.get_daytistics_by_time_updated(
                    settings.DEFAULT_DAYTISTICS_NUMBER_IN_DASHBOARD
                )

        case "createdAt":
            try:
                context["daytistics_list"] = user.get_daytistics_by_time_created(
                    list_size
                )
            except ValueError:
                context["daytistics_list"] = user.get_daytistics_by_time_created(
                    settings.DEFAULT_DAYTISTICS_NUMBER_IN_DASHBOARD
                )

        case "date" | _:
            try:
                context["daytistics_list"] = user.get_daytistics_by_date(list_size)
            except ValueError:
                context["daytistics_list"] = user.get_daytistics_by_date(
                    settings.DEFAULT_DAYTISTICS_NUMBER_IN_DASHBOARD
                )

    return render(request, "daytistics/dashboard.html", context=context)


@login_required
@require_POST
def create_daytistic(request: HttpRequest) -> HttpResponse:
    """
    Create a new daytistic based on the date provided in the request. It is used in the dashboard to create a new daytistic.

    Args:
        request (HttpRequest): The request object

    Returns:
        HttpResponse: The response object
    """
    date_str = request.POST.get("date")

    if not date_str:
        return HttpResponse(
            f"<p class='text-red-500'>{_("Error: Date is missing")}</p>"
        )

    try:
        date = datetime.strptime(date_str, "%d.%m.%Y")
    except ValueError:
        return HttpResponse(f"<p class='text-red-500'>{_("Error: Invalid date")}</p>")

    if Daytistic.objects.filter(user=request.user, date=date).exists():
        return HttpResponse(
            f"<p class='text-red-500'>{_("Error: Daytistic already exists")}</p>"
        )

    if date < datetime.now() - timedelta(weeks=4):
        return HttpResponse(
            f"<p class='text-red-500'>{_("Error: The Daytistic can't be older than 4 weeks")}</p>"
        )

    if date > datetime.now():
        return HttpResponse(
            f"<p class='text-red-500'>{_("Error: Are you watching Back To The Future right now? :D")}</p>"
        )

    Daytistic.objects.create(user=request.user, date=date)

    # TODO: Open edit modal
    return HttpResponse(
        f"<p class='text-green-500'>{_("Daytistic created successfully")}</p>",
        status=201,
    )


@login_required
@require_POST
def add_activity_to_daytistic(request: HttpRequest, daytistic_id: int) -> HttpResponse:
    """
    Add an activity to the daytistic. If the activity already exists, the duration will be added to the existing duration. If the activity does not exist, a new entry will be created.

    Args:
        request (HttpRequest): The request object
        daytistic_id (int): The daytistic id

    Returns:
        HttpResponse: The response object
    """
    duration_pattern = re.compile(r"^\d{2}:\d{2}$")

    try:
        data = json.loads(request.body)
        activity_id = data.get("activity_id")
        duration = data.get("duration")
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    daytistic = get_object_or_404(Daytistic, id=daytistic_id)

    if not Activity.objects.filter(id=activity_id).exists():
        return HttpResponse(
            f"<p class='text-red-500'>{_('Error: Activity not found')}</p>"
        )
    activity = get_object_or_404(Activity, id=activity_id)

    if not re.match(duration_pattern, duration):
        return HttpResponse(
            f"<p class='text-red-500'>{_('Error: Invalid duration format')}</p>"
        )
    duration_timedelta = timedelta(
        hours=int(duration.split(":")[0]), minutes=int(duration.split(":")[1])
    )

    if not daytistic.activities.filter(activity=activity).exists():
        activity_entry = ActivityEntry.objects.create(
            daytistic=daytistic, activity=activity, duration=duration_timedelta
        )
    else:
        activity_entry = daytistic.activities.get(activity=activity)
        activity_entry.duration += duration_timedelta
        activity_entry.save()

    return HttpResponse(
        f"<p class='text-green-500'>{_('Activity added successfully')}</p>", status=201
    )


@login_required
@internal_only
def edit_daytistic(request, daytistic_id):
    if not Daytistic.objects.filter(user=request.user, id=daytistic_id).exists():
        return HttpResponse("Daytistic not found", status=404)

    daytistic = Daytistic.objects.get(user=request.user, id=daytistic_id)

    context = {"daytistic": daytistic}

    return render(request, "daytistics/modal/edit_daytistic.html", context)
