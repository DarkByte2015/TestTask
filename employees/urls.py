from django.conf.urls import url

from . import views

app_name = 'employees'

urlpatterns = [
    url(r'^list/$', views.EmployeesListView.as_view(), name = 'list'),
    url(r'^(?P<pk>[0-9]+)/$', views.EmployeeView.as_view(), name = 'employee')
]
