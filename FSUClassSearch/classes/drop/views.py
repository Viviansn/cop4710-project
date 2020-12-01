from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import connection
from classes.view.views import get_my_classes


@login_required(login_url='login')
def home(request):

    return render(request, 'drop/drop_home.html', {'header': ['Course Reference Number', 'Course ID', 'Section',
            'Name', 'Professor', 'Lecture Days', 'Time Start', 'Time End', 'Location', 'Recitation Days', 'Rec. Time Start',
            'Rec. Time End', 'Recitation Location'],'classes': get_my_classes(request.user.id)})


@login_required(login_url='login')
def drop_success(request):
    if request.method == 'POST':
        deleted_class = request.POST.get('submit')
        user_id = request.user.id

        with connection.cursor() as cursor:
            cursor.execute("""DELETE FROM classes_enrolled_in 
                              WHERE FSUID_id = %s AND course_reference_number_id = %s""",
                              [user_id, deleted_class]
            )
        
        return render(request, 'drop/drop_success.html', {'deleted_class': deleted_class})
    
    return redirect('/classes/drop/')
    