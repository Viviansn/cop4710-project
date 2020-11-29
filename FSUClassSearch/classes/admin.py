from django.contrib import admin
from .models import Student, Professor, Class, Enrolled_In
# Register your models here.

admin.site.register(Student)
admin.site.register(Professor)
admin.site.register(Class)
admin.site.register(Enrolled_In)
