# coding: utf-8

from __future__ import unicode_literals
from django.db import models

class Position(models.Model):
    name = models.CharField('Название', max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'position'
        verbose_name = 'Список должностей'
        verbose_name_plural = 'Списки должностей'

class Department(models.Model):
    name = models.CharField('Название', max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'department'
        verbose_name = 'Список отделов'
        verbose_name_plural = 'Списки отделов'

class Employee(models.Model):
    lastname = models.CharField('Фамилия', max_length=50)
    firstname = models.CharField('Имя', max_length=50)
    secondname = models.CharField('Отчество', max_length=50)
    birthdate = models.DateField('Дата рождения')
    email = models.EmailField('Электронная почта', max_length=50)
    phone = models.CharField('Телефон', max_length=30)
    begin_work = models.DateTimeField('Начало работы')
    end_work = models.DateTimeField('Окончание работы', blank=True, null=True, default=None)
    position = models.ForeignKey(Position)
    department = models.ForeignKey(Department)

    def __str__(self):
        return self.lastname

    class Meta:
        db_table = 'employee'
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'
        ordering = [ 'lastname' ]
