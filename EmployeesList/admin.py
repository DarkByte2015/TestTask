from django.contrib import admin
from .models import Employee, PositionsList, DepartmentsList

# Register your models here.

admin.site.register(Employee)
admin.site.register(PositionsList)
admin.site.register(DepartmentsList)
