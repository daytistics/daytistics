from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Daytistic, ActivityEntry
from django.http import HttpResponse
import datetime

# Create your views here.
@login_required
def dashboard_view(request):
    return render(request, 'main/dashboard.html')

@login_required
def save_daytistic_view(request, entries):
    if request.method == 'POST':
        activities = list()
        for entry in entries:
            activity = ActivityEntry.objects.create(
                user=request.user,
                activity=entry['activity'],
                start_time=entry['start_time'],
                end_time=entry['end_time']
            )

            activities.append(activity.activity)
        
        Daytistic.objects.create(
            user=request.user,
            activities=activities
        )

    return redirect('dashboard')
    #return render(request, 'main/created_daytistic.html')

@login_required
def edit_daytistic_view(request, daytistic_id):

    if not Daytistic.objects.filter(user=request.user, id=daytistic_id).exists():
        return HttpResponse('Daytistic not found', status=404)
    
    return render(request, 'main/edit_daytistic.html')

@login_required
def add_activity_to_daytistic_view(request, daytistic_id):
    if request.method == 'POST':
        daytistic = Daytistic.objects.get(user=request.user, id=daytistic_id)
        
        if not daytistic.date.date() == datetime.date.today():
            return HttpResponse('Daytistic is not from today', status=403)
        
@login_required
def available_activities_view(request):
    response: str = ''

    for activity in request.user.activities.all():
        response += '<option value="' + str(activity.id) + '">' + activity.name + '</option>'

    return HttpResponse(response)

@login_required
def get_todays_activities(request) -> list[ActivityEntry]:
    daytistic = Daytistic.objects.filter(user=request.user, date__date=datetime.date.today())

    if daytistic.exists():
        return daytistic[0].activities.all()
    else:
        return None