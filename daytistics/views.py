# DJANGO IMPORTS
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
# PROJECT IMPORTS
from .models import Daytistic, ActivityEntry
from .storage import EditDaytisticStorage, CurrentEditingsStorage
from activities.models import Activity


# OTHER IMPORTS
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

from django.http import JsonResponse

@login_required
def dashboard_view(request):
    return render(request, 'pages/daytistics/dashboard.html')

@login_required
def create_daytistic(request: HttpRequest) -> HttpResponse:

    if request.method == 'POST':
        date_str = request.POST.get('date')
        if not date_str:
            return HttpResponse("<p class='text-red-500'>Error: Date is missing</p>", status=400)
        try:
            date = datetime.strptime(date_str, '%d.%m.%Y')
        except ValueError:
            return HttpResponse("<p class='text-red-500'>Error: Invalid date</p>", status=400)
        if Daytistic.objects.filter(user=request.user, date=date).exists():
            return HttpResponse("<p class='text-red-500'>Error: Daytistics already exists</p>", status=400)
       
        if date < datetime.now() - timedelta(weeks=4):
            return HttpResponse("<p class='text-red-500'>Error: The daytistic can't be older than 4 weeks</p>", status=400)
       
        if date > datetime.now():
            return HttpResponse("<p class='text-red-500'>Error: The daytistic can't be in the future</p>", status=400)

        daytistic = Daytistic.objects.create(user=request.user, date=date)
        
        response = HttpResponse(status=302)
        response['HX-Redirect'] = reverse('daytistics_edit', args=[daytistic.id])
        return response
   
    return HttpResponse("<p class='text-red-500'>Error: Invalid request</p>", status=400)


# TODO: Tests required as soon as the feature is fully implemented    
@login_required
def edit_daytistic_view(request, daytistic_id):

    if not Daytistic.objects.filter(user=request.user, id=daytistic_id).exists():
        return HttpResponse('Daytistic not found', status=404)
    
    if not request.user == Daytistic.objects.get(id=daytistic_id).user:
        return HttpResponse('Not authorized", status=403')
    
    CurrentEditingsStorage().add_storage(daytistic_id=daytistic_id)

    daytistic = Daytistic.objects.get(user=request.user, id=daytistic_id) 
    for activity_entry in daytistic.activities.all():
        activity_entry.duration_minutes = activity_entry.duration.total_seconds() // 60

    context = {
        'daytistic': Daytistic.objects.get(user=request.user, id=daytistic_id)
    }

    return render(request, 'pages/daytistics/edit_daytistic.html', context)

# TODO: Tests required as soon as the feature is fully implemented   
@login_required
def add_activity_to_daytistic_view(request, daytistic_id):
    if request.method == 'POST':
        daytistic = get_object_or_404(Daytistic, user=request.user, id=daytistic_id)
        
        activity_id = request.POST.get('activity_id')
        duration = request.POST.get('duration')
        
        if not activity_id or not duration:
            return HttpResponse('Missing data', status=400)
        
        try:
            activity_id = int(activity_id)
            duration = int(duration)  # This is in minutes
        except ValueError:
            return HttpResponse('Invalid data', status=400)
        
        activity = get_object_or_404(Activity, id=activity_id)
        duration_timedelta = timedelta(minutes=duration)  # Convert minutes to timedelta
        
        activity_entry, created = ActivityEntry.objects.get_or_create(
            user=request.user,
            activity=activity,
            defaults={'duration': duration_timedelta}
        )
        
        if created:
            daytistic.activities.add(activity_entry)
            return HttpResponse('Activity added', status=200)
        else:
            return HttpResponse('Activity already exists', status=400)
        
    return HttpResponse('Invalid request', status=400)
