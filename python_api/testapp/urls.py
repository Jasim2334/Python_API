from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import Employee

router = DefaultRouter()

router.register(r'EmployeeList', Employee)

urlpatterns = [
    path('', include(router.urls)),
]
