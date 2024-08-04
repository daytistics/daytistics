from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from models import Daytistic, ActivityEntry

# Create your views here.
@login_required
def dashboard_view(request):
    return render(request, 'main/dashboard.html')

@login_required
def create_daytistic_view(request):
    return render(request, 'main/create_daytistic.html')

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