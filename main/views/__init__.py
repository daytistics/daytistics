from .activities import *
from .daytistics import *

from django.contrib.auth.decorators import login_required

@login_required
def dashboard_view(request):
    return render(request, 'main/dashboard.html')





        
