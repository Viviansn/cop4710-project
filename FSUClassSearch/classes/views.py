from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='login')
def home(request):
    user = request.user  #gets the username of currently logged in (useful for adding a class to a student)
    return render(request, 'classes/home.html', {'user':user})

