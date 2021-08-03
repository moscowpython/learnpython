from django.contrib import admin

from .models import (
    MoscowPythonMeetup, LearnPythonCourse, Curators, Feedback, GraduateProjects, GraduateStories,
    LearnPythonCoursePrices, GraduateProjectsVideos, Podcasts, LearnPythonMultiCityCourses
)

admin.site.register(MoscowPythonMeetup)
admin.site.register(LearnPythonCourse)
admin.site.register(Curators)
admin.site.register(Feedback)
admin.site.register(GraduateProjects)
admin.site.register(GraduateStories)
admin.site.register(LearnPythonCoursePrices)
admin.site.register(GraduateProjectsVideos)
admin.site.register(Podcasts)
admin.site.register(LearnPythonMultiCityCourses)