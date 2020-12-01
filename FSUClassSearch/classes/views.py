from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import connection

# Create your views here.
@login_required(login_url='login')
def home(request):

    user_id = request.user.id
    full_name = ()
    with connection.cursor() as cursor:

        cursor.execute("""SELECT first_name, last_name
                        FROM classes_student
                        WHERE classes_student.FSUID_id = %s""", [user_id])
        
        full_name = cursor.fetchall()

    return render(request, 'classes/home.html', {'first_name': full_name[0][0], 'last_name': full_name[0][1]})

