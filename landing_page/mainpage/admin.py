from django.contrib import admin

from .models import CourseReview, Curators, Enrollment, GraduateProjects

admin.site.register(Curators)
admin.site.register(GraduateProjects)
admin.site.register(Enrollment)
admin.site.register(CourseReview)
