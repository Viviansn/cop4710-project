from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='login')
def home(request):
    #database query to search for enrolled classes
    
    return render(request, 'view/view_home.html')
