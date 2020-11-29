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
        cursor.execute("""SELECT course_reference_number, subject_id, number_id, section, first_name, last_name, time_start, time_end, 
                        recitation_time_start, recitation_time_end 
                        FROM classes_class, classes_professor 
                        WHERE classes_class.professor_id_id = classes_professor.FSUID_id""")
        
        results_before_req_check = dictfetchall(cursor)


    if form.cleaned_data["subject_id"] != "":
        with connection.cursor() as cursor:
            cursor.execute("""SELECT course_reference_number, subject_id, number_id, section, first_name, last_name, time_start, time_end, 
                            recitation_time_start, recitation_time_end  
                            FROM classes_class, classes_professor 
                            WHERE classes_class.professor_id_id = classes_professor.FSUID_id AND 
                            classes_class.subject_id = %s""", [form.cleaned_data["subject_id"]])
            
            filter_results = dictfetchall(cursor)
            results_before_req_check = [x for x in results_before_req_check if x in filter_results]

    if form.cleaned_data["number_id"] != "":
        with connection.cursor() as cursor:
            cursor.execute("""SELECT course_reference_number, subject_id, number_id, section, first_name, last_name, time_start, time_end, 
                            recitation_time_start, recitation_time_end  
                            FROM classes_class, classes_professor 
                            WHERE classes_class.professor_id_id = classes_professor.FSUID_id AND 
                            classes_class.number_id = %s""", [form.cleaned_data["number_id"]])
            
            filter_results = dictfetchall(cursor)
            results_before_req_check = [x for x in results_before_req_check if x in filter_results]
    
    if form.cleaned_data["name"] != "":
        with connection.cursor() as cursor:
            cursor.execute("""SELECT course_reference_number, subject_id, number_id, section, first_name, last_name, time_start, time_end, 
                            recitation_time_start, recitation_time_end  
                            FROM classes_class, classes_professor 
                            WHERE classes_class.professor_id_id = classes_professor.FSUID_id AND 
                            classes_class.name = %s""", [form.cleaned_data["name"]])
            
            filter_results = dictfetchall(cursor)
            results_before_req_check = [x for x in results_before_req_check if x in filter_results]


    if form.cleaned_data["course_reference_number"] != "":
        with connection.cursor() as cursor:
            cursor.execute("""SELECT course_reference_number, subject_id, number_id, section, first_name, last_name, time_start, time_end, 
                            recitation_time_start, recitation_time_end  
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
                cursor.execute("""SELECT course_reference_number, subject_id, number_id, section, first_name, last_name, time_start, time_end, 
                                recitation_time_start, recitation_time_end  
                                FROM classes_class, classes_professor 
                                WHERE classes_class.professor_id_id = classes_professor.FSUID_id AND 
                                classes_professor.first_name = %s AND
                                classes_professor.last_name = %s""", [f_name, l_name])
                
                filter_results = dictfetchall(cursor)
                results_before_req_check = [x for x in results_before_req_check if x in filter_results]    
            
    if form.cleaned_data["time_start"] != None:
        with connection.cursor() as cursor:
            #start_timeobj = form.cleaned_data["time_start"].strftime('%H:%M:%S')
            start_timeobj = form.cleaned_data["time_start"]
            end_timeobj = form.cleaned_data["time_end"]
            print("type of start_timeobj is", type(start_timeobj), "value is: ", start_timeobj)
            cursor.execute("""SELECT course_reference_number, subject_id, number_id, section, first_name, last_name, time_start, time_end, 
                            recitation_time_start, recitation_time_end  
                            FROM classes_class, classes_professor 
                            WHERE 
                            classes_class.recitation_time_start BETWEEN %s AND %s""", [start_timeobj, end_timeobj])
            
            filter_results = dictfetchall(cursor)
            results_before_req_check = [x for x in results_before_req_check if x in filter_results]

    #classes_class.recitation_time_start BETWEEN %s AND %s""", [start_timeobj, end_timeobj])
    #WHERE classes_class.professor_id_id = classes_professor.FSUID_id AND 

    # if form.cleaned_data["time_end"] != None:
    #     with connection.cursor() as cursor:
    #         cursor.execute("""SELECT course_reference_number, subject_id, number_id, section, first_name, last_name, time_start, time_end, 
    #                         recitation_time_start, recitation_time_end  
    #                         FROM classes_class, classes_professor 
    #                         WHERE classes_class.professor_id_id = classes_professor.FSUID_id AND 
    #                         classes_class.recitation_time_end <= %s""", [form.cleaned_data["time_end"]])
            
    #         filter_results = dictfetchall(cursor)
    #         results_before_req_check = [x for x in results_before_req_check if x in filter_results]

    


    if (form.cleaned_data["CSBS_Req"] == False and form.cleaned_data["CSBS_Elec"] == False and
        form.cleaned_data["CSBA_Req"] == False and form.cleaned_data["CSBA_Elec"] == False):
            return results_before_req_check


    if form.cleaned_data["CSBS_Req"] == True:
        with connection.cursor() as cursor:
            cursor.execute("""SELECT course_reference_number, subject_id, number_id, section, first_name, last_name, time_start, time_end, 
                            recitation_time_start, recitation_time_end  
                            FROM classes_class, classes_professor 
                            WHERE classes_class.professor_id_id = classes_professor.FSUID_id AND 
                            classes_class.CSBS_Req = TRUE""")
            
            filter_results = dictfetchall(cursor)
            new_results = [x for x in filter_results if x in results_before_req_check]
            #final_results += new_results
            final_results += [x for x in new_results if x not in final_results]

    if form.cleaned_data["CSBS_Elec"] == True:
        with connection.cursor() as cursor:
            cursor.execute("""SELECT course_reference_number, subject_id, number_id, section, first_name, last_name, time_start, time_end, 
                            recitation_time_start, recitation_time_end  
                            FROM classes_class, classes_professor 
                            WHERE classes_class.professor_id_id = classes_professor.FSUID_id AND 
                            classes_class.CSBS_Elec = TRUE""")
            
            filter_results = dictfetchall(cursor)
            new_results = [x for x in filter_results if x in results_before_req_check]
            #final_results += new_results
            final_results += [x for x in new_results if x not in final_results]

    if form.cleaned_data["CSBA_Req"] == True:
        with connection.cursor() as cursor:
            cursor.execute("""SELECT course_reference_number, subject_id, number_id, section, first_name, last_name, time_start, time_end, 
                            recitation_time_start, recitation_time_end  
                            FROM classes_class, classes_professor 
                            WHERE classes_class.professor_id_id = classes_professor.FSUID_id AND 
                            classes_class.CSBA_Req = TRUE""")
            
            filter_results = dictfetchall(cursor)
            new_results = [x for x in filter_results if x in results_before_req_check]
            #final_results += new_results
            final_results += [x for x in new_results if x not in final_results]

    if form.cleaned_data["CSBA_Elec"] == True:
        with connection.cursor() as cursor:
            cursor.execute("""SELECT course_reference_number, subject_id, number_id, section, first_name, last_name, time_start, time_end, 
                            recitation_time_start, recitation_time_end  
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

            return render(request, 'add/results.html', {'header': ['Course Reference Number', 'Course ID', 'Section', 'Time Start', 'Time End', 'Professor'], 'body':get_filtered_classes(form)})
    
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
        '''
        if request.POST.get('1234') == 'Add 1234':
            added_class = request.POST['1234']
        else:
            added_class = None
        
        return render(request, 'add/add_success.html', {'added_class':added_class})
        '''
        added_class = request.POST.get('submit')

        return render(request, 'add/add_success.html', {'added_class':added_class})

    #return render(request, 'add/add_success.html')
    return redirect('/classes/add/')

def can_add_class(ref_num):
    pass