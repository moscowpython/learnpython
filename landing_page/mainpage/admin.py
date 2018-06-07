from django.contrib import admin

from .models import (
	MoscowPythonMeetup, LearnPythonCourse, Courators, Feedback, GraduateProjects,
	GraduateStories, LearnPythonCoursePrices
)

admin.site.register(MoscowPythonMeetup)
admin.site.register(LearnPythonCourse)
admin.site.register(Courators)
admin.site.register(Feedback)
admin.site.register(GraduateProjects)
admin.site.register(GraduateStories)
admin.site.register(LearnPythonCoursePrices)

# Register your models here.
