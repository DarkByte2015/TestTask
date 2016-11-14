from django.conf.urls import url

from . import views

app_name = 'EmployeesList'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^list/$', views.emplist, name = 'emplist'),
    url(r'^employee/(?P<id>[0-9]+)/$', views.employee, name = 'employee')
]
