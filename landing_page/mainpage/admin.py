from django.contrib import admin

from .models import (
	MoscowPythonMeetup, LearnPythonCourse, Courators, Feedback, GraduateProjects
)

admin.site.register(MoscowPythonMeetup)
admin.site.register(LearnPythonCourse)
admin.site.register(Courators)
admin.site.register(Feedback)
admin.site.register(GraduateProjects)

# Register your models here.
