from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Employee(models.Model):
    secondname = models.CharField(max_length=50)
    firstname = models.CharField(max_length=50)
    middlename = models.CharField(max_length=50)
    birthdate = models.DateField()
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=15)
    begin_work = models.DateTimeField()
    end_work = models.DateTimeField()
    position = models.CharField(max_length=50)
    department = models.CharField(max_length=50)

    def __str__(self):
        return self.secondname

    class Meta:
        db_table = 'employee'
