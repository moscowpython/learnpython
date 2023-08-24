from django.contrib import admin

from .models import Curators, Enrollment, GraduateProjects

admin.site.register(Curators)
admin.site.register(GraduateProjects)
admin.site.register(Enrollment)
