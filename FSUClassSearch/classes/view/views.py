from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import connection
from classes.add.views import dictfetchall

@login_required(login_url='login')
def home(request):
    
    user_id = request.user.id
    num_classes = ()
    with connection.cursor() as cursor:
        cursor.execute("""SELECT COUNT(*)
                          FROM classes_enrolled_in
                          WHERE FSUID_id = %s""", [user_id])
        num_classes = cursor.fetchall()

    return render(request, 'view/view_home.html', {'header': ['Course Reference Number', 'Course ID', 'Section',
            'Name', 'Professor', 'Lecture Days', 'Time Start', 'Time End', 'Location', 'Recitation Days', 'Rec. Time Start',
            'Rec. Time End', 'Recitation Location'],'classes': get_my_classes(user_id), 'num_classes': num_classes[0][0]})


def get_my_classes(user_id):
    my_classes = ()
    with connection.cursor() as cursor:
        cursor.execute("""SELECT course_reference_number, name, subject_id, number_id, section, first_name,
                        last_name, lec_days, time_start, time_end, location, rec_day, recitation_time_start,
                        recitation_time_end, recitation_location
                        FROM classes_enrolled_in, classes_class, classes_professor 
                        WHERE classes_enrolled_in.FSUID_id = %s AND 
                        classes_enrolled_in.course_reference_number_id = classes_class.course_reference_number AND
                        classes_class.professor_id_id = classes_professor.FSUID_id""", [user_id])

        my_classes = dictfetchall(cursor)

    return my_classes

