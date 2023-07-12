from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(ExportDataLogs)
admin.site.register(Customers)
admin.site.register(Productlines)
admin.site.register(Payments)
admin.site.register(Products)
admin.site.register(Orders)
admin.site.register(Orderdetails)
admin.site.register(Offices)
admin.site.register(Employees)

