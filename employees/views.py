# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404
from django.views import generic
import json
from .models import Employee, Position, Department
from . import utils

class EmployeesListView(generic.ListView):
    template_name = 'employees/employees_list.html'
    model = Employee

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['groups'] = list(utils.compute_groups('А', 'Я'))
        context['departments'] = Department.objects.all()
        context['selected_group'] = context['groups'][0]['id']
        context['is_work'] = False
        context['selected_departments'] = [ d.pk for d in context['departments']]
        data = self.request.GET

        if data:
            tmp = data.get('selected_group', context['selected_group'])
            context['selected_group'] = int(tmp)

            tmp = data.get('is_work', context['is_work'])
            context['is_work'] = not tmp != 'on'

            tmp = data.getlist('selected_departments', context['selected_departments'])
            context['selected_departments'] = [ int(d) for d in tmp ]

        context['employees'] = utils.get_employees(context)
        return context

class EmployeeView(generic.DetailView):
    template_name = 'employees/employee.html'
    context_object_name = 'employee'

    def get_object(self, queryset = None):
        return get_object_or_404(Employee, pk = self.kwargs['pk'])
