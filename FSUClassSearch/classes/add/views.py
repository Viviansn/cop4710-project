from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . import forms
from django.db import connection
# Create your views here.

@login_required(login_url='login')
def home(request):
    
    return render(request, 'add/add_home.html', {'form': forms.SearchFilterForm()})


def get_filtered_classes(form):
    #cumul_results_filled = False
    filter_results = []
    results_before_req_check = []
    final_results = []
    with connection.cursor() as cursor:
        cursor.execute("""SELECT course_reference_number, name, subject_id, number_id, section, first_name, last_name, lec_days, time_start, time_end, 
                        rec_day, recitation_time_start, recitation_time_end 
                        FROM classes_class, classes_professor 
                        WHERE classes_class.professor_id_id = classes_professor.FSUID_id""")
        
        results_before_req_check = dictfetchall(cursor)


    if form.cleaned_data["subject_id"] != "":
        with connection.cursor() as cursor:
            cursor.execute("""SELECT course_reference_number, name, subject_id, number_id, section, first_name, last_name, lec_days, time_start, time_end, 
                            rec_day, recitation_time_start, recitation_time_end 
                            FROM classes_class, classes_professor 
                            WHERE classes_class.professor_id_id = classes_professor.FSUID_id AND 
                            classes_class.subject_id = %s""", [form.cleaned_data["subject_id"]])
            
            filter_results = dictfetchall(cursor)
            results_before_req_check = [x for x in results_before_req_check if x in filter_results]

    if form.cleaned_data["number_id"] != "":
        with connection.cursor() as cursor:
            cursor.execute("""SELECT course_reference_number, name, subject_id, number_id, section, first_name, last_name, lec_days, time_start, time_end, 
                            rec_day, recitation_time_start, recitation_time_end  
                            FROM classes_class, classes_professor 
                            WHERE classes_class.professor_id_id = classes_professor.FSUID_id AND 
                            classes_class.number_id = %s""", [form.cleaned_data["number_id"]])
            
            filter_results = dictfetchall(cursor)
            results_before_req_check = [x for x in results_before_req_check if x in filter_results]
    
    if form.cleaned_data["name"] != "":
        with connection.cursor() as cursor:
            cursor.execute("""SELECT course_reference_number, name, subject_id, number_id, section, first_name, last_name, lec_days, time_start, time_end, 
                            rec_day, recitation_time_start, recitation_time_end  
                            FROM classes_class, classes_professor 
                            WHERE classes_class.professor_id_id = classes_professor.FSUID_id AND 
                            classes_class.name = %s""", [form.cleaned_data["name"]])
            
            filter_results = dictfetchall(cursor)
            results_before_req_check = [x for x in results_before_req_check if x in filter_results]


    if form.cleaned_data["course_reference_number"] != "":
        with connection.cursor() as cursor:
            cursor.execute("""SELECT course_reference_number, name, subject_id, number_id, section, first_name, last_name, lec_days, time_start, time_end, 
                            rec_day, recitation_time_start, recitation_time_end  
                            FROM classes_class, classes_professor 
                            WHERE classes_class.professor_id_id = classes_professor.FSUID_id AND 
                            classes_class.course_reference_number = %s""", [form.cleaned_data["course_reference_number"]])
            
            filter_results = dictfetchall(cursor)
            results_before_req_check = [x for x in results_before_req_check if x in filter_results]
    
    if form.cleaned_data["professor"] != "":
        prof_full_name = form.cleaned_data["professor"].split()
        #print(prof_full_name)
        #name_split = prof_full_name.split()
        #print("prof_full_name = ", name_split)
        if len(prof_full_name) == 2:
            f_name = prof_full_name[0]
            l_name = prof_full_name[1]

            with connection.cursor() as cursor:
                cursor.execute("""SELECT course_reference_number, name, subject_id, number_id, section, first_name, last_name, lec_days, time_start, time_end, 
                                rec_day, recitation_time_start, recitation_time_end 
                                FROM classes_class, classes_professor 
                                WHERE classes_class.professor_id_id = classes_professor.FSUID_id AND 
                                classes_professor.first_name = %s AND
                                classes_professor.last_name = %s""", [f_name, l_name])
                
                filter_results = dictfetchall(cursor)
                results_before_req_check = [x for x in results_before_req_check if x in filter_results]    
            
    if form.cleaned_data["time_start"] != None:
        with connection.cursor() as cursor:
            
            start_timeobj = form.cleaned_data["time_start"]
            print("type of start_timeobj is", type(start_timeobj), "value is: ", start_timeobj)
            cursor.execute("""SELECT course_reference_number, name, subject_id, number_id, section, first_name, last_name, lec_days, time_start, time_end, 
                            rec_day, recitation_time_start, recitation_time_end 
                            FROM classes_class, classes_professor 
                            WHERE classes_class.professor_id_id = classes_professor.FSUID_id AND
                            classes_class.time_start >= %s""", [start_timeobj])
            
            filter_results = dictfetchall(cursor)
            results_before_req_check = [x for x in results_before_req_check if x in filter_results]

    #classes_class.recitation_time_start BETWEEN %s AND %s""", [start_timeobj, end_timeobj])
   

    if form.cleaned_data["time_end"] != None:
        with connection.cursor() as cursor:
            cursor.execute("""SELECT course_reference_number, name, subject_id, number_id, section, first_name, last_name, lec_days, time_start, time_end, 
                            rec_day, recitation_time_start, recitation_time_end  
                            FROM classes_class, classes_professor 
                            WHERE classes_class.professor_id_id = classes_professor.FSUID_id AND 
                            classes_class.recitation_time_end <= %s""", [form.cleaned_data["time_end"]])
            
            filter_results = dictfetchall(cursor)
            results_before_req_check = [x for x in results_before_req_check if x in filter_results]

    

    if (form.cleaned_data["CSBS_Req"] == False and form.cleaned_data["CSBS_Elec"] == False and
        form.cleaned_data["CSBA_Req"] == False and form.cleaned_data["CSBA_Elec"] == False):
            return results_before_req_check


    if form.cleaned_data["CSBS_Req"] == True:
        with connection.cursor() as cursor:
            cursor.execute("""SELECT course_reference_number, name, subject_id, number_id, section, first_name, last_name, lec_days, time_start, time_end, 
                            rec_day, recitation_time_start, recitation_time_end  
                            FROM classes_class, classes_professor 
                            WHERE classes_class.professor_id_id = classes_professor.FSUID_id AND 
                            classes_class.CSBS_Req = TRUE""")
            
            filter_results = dictfetchall(cursor)
            new_results = [x for x in filter_results if x in results_before_req_check]
            #final_results += new_results
            final_results += [x for x in new_results if x not in final_results]

    if form.cleaned_data["CSBS_Elec"] == True:
        with connection.cursor() as cursor:
            cursor.execute("""SELECT course_reference_number, name, subject_id, number_id, section, first_name, last_name, lec_days, time_start, time_end, 
                            rec_day, recitation_time_start, recitation_time_end  
                            FROM classes_class, classes_professor 
                            WHERE classes_class.professor_id_id = classes_professor.FSUID_id AND 
                            classes_class.CSBS_Elec = TRUE""")
            
            filter_results = dictfetchall(cursor)
            new_results = [x for x in filter_results if x in results_before_req_check]
            #final_results += new_results
            final_results += [x for x in new_results if x not in final_results]

    if form.cleaned_data["CSBA_Req"] == True:
        with connection.cursor() as cursor:
            cursor.execute("""SELECT course_reference_number, name, subject_id, number_id, section, first_name, last_name, lec_days, time_start, time_end, 
                            rec_day, recitation_time_start, recitation_time_end 
                            FROM classes_class, classes_professor 
                            WHERE classes_class.professor_id_id = classes_professor.FSUID_id AND 
                            classes_class.CSBA_Req = TRUE""")
            
            filter_results = dictfetchall(cursor)
            new_results = [x for x in filter_results if x in results_before_req_check]
            #final_results += new_results
            final_results += [x for x in new_results if x not in final_results]

    if form.cleaned_data["CSBA_Elec"] == True:
        with connection.cursor() as cursor:
            cursor.execute("""SELECT course_reference_number, name, subject_id, number_id, section, first_name, last_name, lec_days, time_start, time_end, 
                            rec_day, recitation_time_start, recitation_time_end  
                            FROM classes_class, classes_professor 
                            WHERE classes_class.professor_id_id = classes_professor.FSUID_id AND 
                            classes_class.CSBA_Elec = TRUE""")
            
            filter_results = dictfetchall(cursor)
            new_results = [x for x in filter_results if x in results_before_req_check]
            #final_results += new_results
            final_results += [x for x in new_results if x not in final_results]


    return final_results
        


    

def get_all_fields_from_form(instance):
    fields = list(instance.base_fields)
    for field in list(instance.declared_fields):
        if field not in fields:
            fields.append(field)
    
    return fields


@login_required(login_url='login')
def results(request):
    if request.method == 'POST':
        form = forms.SearchFilterForm(request.POST)
        if form.is_valid():
            #valid_form = form
            all_fields = get_all_fields_from_form(forms.SearchFilterForm())
            print(all_fields)
            for field in get_all_fields_from_form(forms.SearchFilterForm()):
                print(field, form.cleaned_data[field])
            
            print('\n\n\n', get_filtered_classes(form))

            return render(request, 'add/results.html', {'header': ['Course Reference Number', 'Course ID', 'Section', 'Name', 'Professor', 'Lecture Days', 'Time Start', 'Time End', 'Recitation Days', 'Rec. Time Start', 'Rec. Time End'], 'body':get_filtered_classes(form)})
    
    #course_reference_number, name, subject_id, number_id, section, first_name, last_name, lec_days, time_start, time_end, 
                            #rec_day, recitation_time_start, recitation_time_end

    #return render(request, 'add/results.html')
    return redirect('/classes/add/')




def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


@login_required(login_url='login')
def add_success(request):
    if request.method == 'POST':
       
        added_class = request.POST.get('submit')
        print('\n\nadded_class = ', added_class)
        days = ()
        times = ()
        with connection.cursor() as cursor:
            cursor.execute("""SELECT lec_mo, lec_tu, lec_we, lec_th, lec_fr, 
                            rec_mo, rec_tu, rec_we, rec_th, rec_fr
                            FROM classes_class
                            WHERE course_reference_number = %s""", [added_class])
            
            days = cursor.fetchall()

        with connection.cursor() as cursor:
            cursor.execute("""SELECT time_start, time_end, recitation_time_start, recitation_time_end
                            FROM classes_class
                            WHERE course_reference_number = %s""", [added_class])
            
            times = cursor.fetchall()

        print('days = ', days)
        print('times = ', times)
        
        user_id = request.user.id

        # the_response = []

        # with connection.cursor() as cursor:
        #     cursor.execute("""SELECT course_reference_number
        #                     FROM classes_class
        #                     WHERE rec_we = TRUE AND %s = TRUE""", [days[0][7]])
            
        #     the_response = cursor.fetchall()

        # print('the response = ', the_response)


###############################################################################################


        # the_response = []

        # with connection.cursor() as cursor:
        #     cursor.execute("""SELECT course_reference_number, name
        #                     FROM classes_enrolled_in, classes_class
        #                     WHERE classes_enrolled_in.FSUID_id = %s AND classes_enrolled_in.course_reference_number_id = classes_class.course_reference_number""", [user_id])
            
        #     the_response = cursor.fetchall()

        # print('user_id = ', user_id)
        # print('the response = ', the_response)

#WHERE classes_enrolled_in.FSUID_id = %s AND classes_enrolled_in.course_reference_number_id = classes_class.course_reference_number""", [user_id])

##################################################################
        
        course_conflicts_with_new_course = ()

        with connection.cursor() as cursor:
            cursor.execute("""SELECT course_reference_number 
                            FROM classes_enrolled_in, classes_class
                            WHERE classes_enrolled_in.FSUID_id = %s AND classes_enrolled_in.course_reference_number_id = classes_class.course_reference_number AND
                            (
                                (
                                    (lec_mo = TRUE) AND (%s = TRUE) AND ((%s BETWEEN time_start AND time_end) OR (time_start BETWEEN %s AND %s))
                                )
                                OR
                                (
                                    (lec_mo = TRUE) AND (%s = TRUE) AND ((%s BETWEEN time_start AND time_end) OR (time_start BETWEEN %s AND %s))
                                )
                                OR
                                (
                                    (rec_mo = TRUE) AND (%s = TRUE) AND ((%s BETWEEN recitation_time_start AND recitation_time_end) OR (recitation_time_start BETWEEN %s AND %s))
                                )
                                OR
                                (
                                    (rec_mo = TRUE) AND (%s = TRUE) AND ((%s BETWEEN recitation_time_start AND recitation_time_end) OR (recitation_time_start BETWEEN %s AND %s))
                                )
                                OR
                                (
                                    (lec_tu = TRUE) AND (%s = TRUE) AND ((%s BETWEEN time_start AND time_end) OR (time_start BETWEEN %s AND %s))
                                )
                                OR
                                (
                                    (lec_tu = TRUE) AND (%s = TRUE) AND ((%s BETWEEN time_start AND time_end) OR (time_start BETWEEN %s AND %s))
                                )
                                OR
                                (
                                    (rec_tu = TRUE) AND (%s = TRUE) AND ((%s BETWEEN recitation_time_start AND recitation_time_end) OR (recitation_time_start BETWEEN %s AND %s))
                                )
                                OR
                                (
                                    (rec_tu = TRUE) AND (%s = TRUE) AND ((%s BETWEEN recitation_time_start AND recitation_time_end) OR (recitation_time_start BETWEEN %s AND %s))
                                )
                                OR
                                (
                                    (lec_we = TRUE) AND (%s = TRUE) AND ((%s BETWEEN time_start AND time_end) OR (time_start BETWEEN %s AND %s))
                                )
                                OR
                                (
                                    (lec_we = TRUE) AND (%s = TRUE) AND ((%s BETWEEN time_start AND time_end) OR (time_start BETWEEN %s AND %s))
                                )
                                OR
                                (
                                    (rec_we = TRUE) AND (%s = TRUE) AND ((%s BETWEEN recitation_time_start AND recitation_time_end) OR (recitation_time_start BETWEEN %s AND %s))
                                )
                                OR
                                (
                                    (rec_we = TRUE) AND (%s = TRUE) AND ((%s BETWEEN recitation_time_start AND recitation_time_end) OR (recitation_time_start BETWEEN %s AND %s))
                                )
                                OR
                                (
                                    (lec_th = TRUE) AND (%s = TRUE) AND ((%s BETWEEN time_start AND time_end) OR (time_start BETWEEN %s AND %s))
                                )
                                OR
                                (
                                    (lec_th = TRUE) AND (%s = TRUE) AND ((%s BETWEEN time_start AND time_end) OR (time_start BETWEEN %s AND %s))
                                )
                                OR
                                (
                                    (rec_th = TRUE) AND (%s = TRUE) AND ((%s BETWEEN recitation_time_start AND recitation_time_end) OR (recitation_time_start BETWEEN %s AND %s))
                                )
                                OR
                                (
                                    (rec_th = TRUE) AND (%s = TRUE) AND ((%s BETWEEN recitation_time_start AND recitation_time_end) OR (recitation_time_start BETWEEN %s AND %s))
                                )
                                OR
                                (
                                    (lec_fr = TRUE) AND (%s = TRUE) AND ((%s BETWEEN time_start AND time_end) OR (time_start BETWEEN %s AND %s))
                                )
                                OR
                                (
                                    (lec_fr = TRUE) AND (%s = TRUE) AND ((%s BETWEEN time_start AND time_end) OR (time_start BETWEEN %s AND %s))
                                )
                                OR
                                (
                                    (rec_fr = TRUE) AND (%s = TRUE) AND ((%s BETWEEN recitation_time_start AND recitation_time_end) OR (recitation_time_start BETWEEN %s AND %s))
                                )
                                OR
                                (
                                    (rec_fr = TRUE) AND (%s = TRUE) AND ((%s BETWEEN recitation_time_start AND recitation_time_end) OR (recitation_time_start BETWEEN %s AND %s))
                                )

                            )
                            """, [user_id, days[0][0], times[0][0], times[0][0], times[0][1], 
                                           days[0][5], times[0][2], times[0][2], times[0][3],
                                           days[0][0], times[0][0], times[0][0], times[0][1],
                                           days[0][5], times[0][2], times[0][2], times[0][3],

                                           days[0][1], times[0][0], times[0][0], times[0][1], 
                                           days[0][6], times[0][2], times[0][2], times[0][3],
                                           days[0][1], times[0][0], times[0][0], times[0][1],
                                           days[0][6], times[0][2], times[0][2], times[0][3],

                                           days[0][2], times[0][0], times[0][0], times[0][1], 
                                           days[0][7], times[0][2], times[0][2], times[0][3],
                                           days[0][2], times[0][0], times[0][0], times[0][1],
                                           days[0][7], times[0][2], times[0][2], times[0][3],

                                           days[0][3], times[0][0], times[0][0], times[0][1], 
                                           days[0][8], times[0][2], times[0][2], times[0][3],
                                           days[0][3], times[0][0], times[0][0], times[0][1],
                                           days[0][8], times[0][2], times[0][2], times[0][3],

                                           days[0][4], times[0][0], times[0][0], times[0][1], 
                                           days[0][9], times[0][2], times[0][2], times[0][3],
                                           days[0][4], times[0][0], times[0][0], times[0][1],
                                           days[0][9], times[0][2], times[0][2], times[0][3],

             ])

            print('days[0][0] = ', days[0][0])
            print('days[0][1] = ', days[0][1])
            print('days[0][2] = ', days[0][2])
            print('days[0][3] = ', days[0][3])
            print('days[0][4] = ', days[0][4])
            print('days[0][5] = ', days[0][5])
            print('days[0][6] = ', days[0][6])
            print('days[0][7] = ', days[0][7])
            print('days[0][8] = ', days[0][8])
            print('days[0][9] = ', days[0][9])
            print('times[0][0] = ', times[0][0])
            print('times[0][1] = ', times[0][1])
            print('times[0][2] = ', times[0][2])
            print('times[0][3] = ', times[0][3])
            course_conflicts_with_new_course = cursor.fetchall()
            print(course_conflicts_with_new_course)

        if not course_conflicts_with_new_course:
            print("\n\n\nYES IT WORKED!!!!!!!!!!!!!\n")
            return render(request, 'add/add_success.html', {'added_class':added_class})
        else:
            print('COULDN''T ADD CLASS B/C OF SCHEDULING CONFLICT')
            return render(request, 'add/add_fail.html', {'failed_class':added_class})

#######################################################################

        #return render(request, 'add/add_success.html', {'added_class':added_class})

    #return render(request, 'add/add_success.html')
    return redirect('/classes/add/')


@login_required(login_url='login')
def add_fail(request):
    if request.method == 'POST':
        pass
    return redirect('/classes/add/')


def can_add_class(ref_num):
    pass