from django.db import models


class Employee(models.Model):
    name = models.CharField(max_length=60)
    employee_code = models.CharField(max_length=80, primary_key=True)


class Vendor(models.Model):
    name = models.CharField(max_length=60)
    vendor_code = models.CharField(max_length=80, primary_key=True)


class Expense(models.Model):
    employee_code = models.ForeignKey(Employee, on_delete=models.CASCADE)
    vendor_code = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    expense_comment = models.CharField(max_length=255)
    expense_done_on = models.DateField()
    expense_amount = models.IntegerField()

