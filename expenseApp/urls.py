from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path(r'^get-employee/$', views.employee),
    re_path(r'^get-vendor/$', views.vendor),
    re_path(r'^get-expense-for-vendor/$', views.vendor_expense),
    re_path(r'^get-expense-for-employee/$', views.employee_expense),
    path('add-employee/', views.employee),
    path('add-vendor/', views.vendor),
    path('add-expense/', views.expense),
]