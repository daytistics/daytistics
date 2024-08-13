# DJANGO IMPORTS
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.decorators import login_required
from main.models import Activity

@login_required
def available_activities_view(request):
    response: str = ''

    for activity in request.user.activities.all():
        response += '<option value="' + str(activity.id) + '">' + activity.name + '</option>'

    for activity in Activity.objects.filter(is_global=True):
        response += '<option value="' + str(activity.id) + '">' + activity.name + '</option>'

    return HttpResponse(response)