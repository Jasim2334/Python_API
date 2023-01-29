from django.contrib import admin
from .models import Person, Address, WorkExperience, Qualification, Project

admin.site.register(Person)
admin.site.register(Address)
admin.site.register(WorkExperience)
admin.site.register(Qualification)
admin.site.register(Project)
