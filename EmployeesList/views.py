# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.template import RequestContext, loader
import re
from .models import Employee

# Create your views here.

def index(request):
    lranges = [ ('А', 'Г'), ('Д', 'Ж'), ('З', 'К'), ('Л', 'П'), ('Р', 'У'), ('Ф', 'Я') ]
    employees = Employee.objects.all()
    ranges = []

    for b, e in lranges:
        r = r'^[%s-%s].{0,}' % (b.lower(), e.lower())
        l = [h for h in employees if re.match(r, h.secondname.lower())]
        rng = (b, e, l)
        ranges.append(rng)

    return render(request, 'EmployeesList/index.html', { 'ranges' : ranges })

def employee(request, id):
    emp = get_object_or_404(Employee, pk=id)
    return HttpResponse(emp)
