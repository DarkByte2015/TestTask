from __future__ import unicode_literals
from django.db import models
#from binascii import crc32
import binascii

# Create your models here.

class Employee(models.Model):
    secondname = models.CharField('Фамилия', max_length=50)
    firstname = models.CharField('Имя', max_length=50)
    middlename = models.CharField('Отчество', max_length=50)
    birthdate = models.DateField('Дата рождения')
    email = models.EmailField('Электронная почта', max_length=50)
    phone = models.CharField('Телефон', max_length=15)
    begin_work = models.DateTimeField('Начало работы')
    end_work = models.DateTimeField('Окончание работы')
    position = models.CharField('Должность', max_length=50)
    department = models.CharField('Отдел', max_length=50)

    depid = property()

    @depid.getter
    def depid(self):
        return str(binascii.crc32(self.department.encode()))

    is_working = property()

    @is_working.getter
    def is_working(self):
        return str(len(str(self.end_work)) == 0).lower()

    def __str__(self):
        return self.secondname

    class Meta:
        db_table = 'employee'
        verbose_name = 'сотрудник'
        verbose_name_plural = 'сотрудники'
