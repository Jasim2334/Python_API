from rest_framework import viewsets
from .models import Person, Address, WorkExperience, Qualification, Project
from .serializers import PersonSerializer

class Employee(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
