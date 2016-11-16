# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.template import RequestContext, loader
from binascii import crc32
import re
from .models import Employee

# Create your views here.

def index(request):
    return render(request, 'EmployeesList/index.html')

def emplist(request):
    lranges = [ ('А', 'Г'), ('Д', 'Ж'), ('З', 'К'), ('Л', 'П'), ('Р', 'У'), ('Ф', 'Я') ]
    employees = Employee.objects.all()
    ranges = []

    for b, e in lranges:
        r = r'^[%s-%s].{0,}' % (b.lower(), e.lower())
        l = [h for h in employees if re.match(r, h.secondname.lower())]
        gid = ord(b)
        rng = (b, e, l, gid)
        ranges.append(rng)

    return render(request, 'EmployeesList/emplist.html', { 'ranges' : ranges })

def employee(request, id):
    emp = get_object_or_404(Employee, pk=id)
    return render(request, 'EmployeesList/employee.html', { 'employee' : emp })
