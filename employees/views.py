# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404
from django.views import generic
import json
from .models import Employee, Position, Department
from . import utils

class EmployeesListView(generic.ListView):
    template_name = 'employees/employees_list.html'
    model = Employee

    def __init__(self):
        employees = [ e.lastname for e in Employee.objects.all() ]
        letters, avg = utils.distribute_by_letters(employees)
        groups = utils.distribute_by_groups(letters, avg)
        groups = [ g[0] for g in groups]
        self._groups = []

        for index, key in enumerate(groups):
            begin, end = tuple(key.split('-'))

            group = {
                'id': index,
                'letters': utils.letter_range(begin, end),
                'begin': begin,
                'end': end,
                'range': key
            }

            self._groups.append(group)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['groups'] = self._groups
        context['departments'] = Department.objects.all()
        context['selected_group'] = [ 0 ]
        context['is_work'] = False
        context['selected_departments'] = [ d.pk for d in context['departments']]
        data = self.request.GET

        if data:
            context['selected_group'] = data.get('selected_group', context['selected_group'])
            context['selected_group'] = [ int(g) for g in context['selected_group'] ]

            context['is_work'] = data.get('is_work', context['is_work'])
            context['is_work'] = not context['is_work'] != 'on'

            context['selected_departments'] = data.getlist('selected_departments', context['selected_departments'])
            context['selected_departments'] = [ int(d) for d in context['selected_departments'] ]

        print(context['is_work'])
        context['selected_group'] = context['selected_group'][0]
        q = utils.get_employees(context)
        context['employees'] = Employee.objects.filter(q)
        return context

class EmployeeView(generic.DetailView):
    template_name = 'employees/employee.html'
    context_object_name = 'employee'

    def get_object(self, queryset = None):
        return get_object_or_404(Employee, pk = self.kwargs['pk'])
