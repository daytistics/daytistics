# DJANGO IMPORTS
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import get_object_or_404
# PROJECT IMPORTS
from .models import Daytistic, ActivityEntry
from .storage import CurrentEditingsStorage
from activities.models import Activity


# OTHER IMPORTS
from datetime import datetime, timedelta
from django.utils.translation import gettext_lazy as _

@login_required
def dashboard_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'daytistics/dashboard.html')

# TODO: Translate
@login_required
@require_POST
def create_daytistic(request: HttpRequest) -> HttpResponse:
    date_str = request.POST.get('date')

    if not date_str:
        return HttpResponse(f"<p class='text-red-500'>{_("Error: Date is missing")}</p>")
    
    try:
        date = datetime.strptime(date_str, '%d.%m.%Y')
    except ValueError:
        return HttpResponse(f"<p class='text-red-500'>{_("Error: Invalid date")}</p>")
    
    if Daytistic.objects.filter(user=request.user, date=date).exists():
        return HttpResponse(f"<p class='text-red-500'>{_("Error: Daytistic already exists")}</p>")
    
    if date < datetime.now() - timedelta(weeks=4):
        return HttpResponse(f"<p class='text-red-500'>{_("Error: The Daytistic can't be older than 4 weeks")}</p>")
    
    if date > datetime.now():
        return HttpResponse(f"<p class='text-red-500'>{_("Error: Are you watching Back To The Future right now? :D")}</p>")

    daytistic = Daytistic.objects.create(user=request.user, date=date)
    
    response = HttpResponse(status=302)
    response['HX-Redirect'] = reverse('daytistics_edit', args=[daytistic.id])
    return response
   


# TODO: Tests required as soon as the feature is fully implemented    
@login_required
def edit_daytistic_view(request, daytistic_id):

    if not Daytistic.objects.filter(user=request.user, id=daytistic_id).exists():
        return HttpResponse('Daytistic not found', status=404)
    
    if not request.user == Daytistic.objects.get(id=daytistic_id).user:
        return HttpResponse("Not authorized", status=403)
    
    CurrentEditingsStorage().add_storage(daytistic_id=daytistic_id)

    daytistic = Daytistic.objects.get(user=request.user, id=daytistic_id) 
    for activity_entry in daytistic.activities.all():
        activity_entry.duration_minutes = activity_entry.duration.total_seconds() // 60

    context = {
        'daytistic': Daytistic.objects.get(user=request.user, id=daytistic_id)
    }

    return render(request, 'daytistics/edit_daytistic.html', context)

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
