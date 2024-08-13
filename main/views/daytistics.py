# DJANGO IMPORTS
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
# PROJECT IMPORTS
from ..models import Daytistic, ActivityEntry, Activity
from ..storage import EditDaytisticStorage, CurrentEditingsStorage


# OTHER IMPORTS
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

from django.http import JsonResponse


@login_required
def create_daytistic(request: HttpRequest) -> HttpResponse:

    import time
    time.sleep(4)
    return JsonResponse({'message': 'Daytistic created'})

    if request.method == 'POST':
        date_str = request.POST.get('date')
        logger.info(f"Empfangene POST-Anfrage mit Datum: {date_str}")
        if not date_str:
            return HttpResponse("<p class='text-red-500'>Fehler: Datum fehlt</p>")
        try:
            date = datetime.strptime(date_str, '%d.%m.%Y')
        except ValueError:
            return HttpResponse("<p class='text-red-500'>Fehler: Ungültiges Datum</p>")
        if Daytistic.objects.filter(user=request.user, date=date).exists():
            return HttpResponse("<p class='text-red-500'>Fehler: Daytistic existiert bereits</p>")
       
        if date < datetime.now() - timedelta(weeks=4):
            return HttpResponse("<p class='text-red-500'>Fehler: Daytistic kann nicht älter als 4 Wochen sein</p>")
       
        daytistic = Daytistic.objects.create(user=request.user, date=date)
        print(f"Daytistic erfolgreich erstellt für Datum: {date} und Benutzer: {request.user}")
        
        # Render the edit_daytistic template as a string
        edit_daytistic_html = render_to_string('main/edit_daytistic.html', {'daytistic': daytistic}, request=request)
        
        print(f"HTML-Template für edit_daytistic gerendert")
        # Return the rendered HTML along with a redirect instruction for HTMX
        response = HttpResponse()
        response['HX-Redirect'] = reverse('edit_daytistic', args=[daytistic.id])
        return response
   
    return HttpResponse("<p class='text-red-500'>Fehler: Ungültige Anfrage</p>")

        
@login_required
def add_activity_to_daytistic_view(request, daytistic_id):
    if request.method == 'POST':
        daytistic = Daytistic.objects.get(user=request.user, id=daytistic_id)
        
        if not daytistic.date.date() == datetime.date.today():
            return HttpResponse('Daytistic is not from today', status=403)
        
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

    return render(request, 'main/edit_daytistic.html', context)

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
