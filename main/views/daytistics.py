from datetime import datetime, timedelta
from django.http import HttpResponse, HttpRequest
from models import Daytistic

def create_daytistic(request: HttpRequest, date: datetime):

    if request.method == 'POST':
        if Daytistic.objects.filter(user=request.user, date=date).exists():
            return HttpResponse("", status=400)
        
        if date < datetime.now() - 
            return HttpResponse("", status=400)
        
