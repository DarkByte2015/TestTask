from __future__ import unicode_literals
from django.db import models
from binascii import crc32

# Create your models here.

class Employee(models.Model):
    secondname = models.CharField('Фамилия', max_length=50)
    firstname = models.CharField('Имя', max_length=50)
    middlename = models.CharField('Отчество', max_length=50)
    birthdate = models.DateField('Дата рождения')
    email = models.EmailField('Электронная почта', max_length=50)
    phone = models.CharField('Телефон', max_length=15)
    begin_work = models.DateTimeField('Начало работы')
    end_work = models.DateTimeField('Окончание работы', blank=True, null=True, default=None)
    position = models.ForeignKey('PositionsList')
    department = models.ForeignKey('DepartmentsList')

    @property
    def depid(self):
        return str(crc32(self.department.name.encode()))

    @property
    def is_working(self):
        return str(self.end_work == None).lower()

    def __str__(self):
        return self.secondname

    class Meta:
        db_table = 'employee'
        verbose_name = 'сотрудник'
        verbose_name_plural = 'сотрудники'

class PositionsList(models.Model):
    name = models.CharField('Название', max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'positions_list'
        verbose_name = 'Список должностей'
        verbose_name_plural = 'Списки должностей'

class DepartmentsList(models.Model):
    name = models.CharField('Название', max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'departments_list'
        verbose_name = 'Список отделов'
        verbose_name_plural = 'Списки отделов'
