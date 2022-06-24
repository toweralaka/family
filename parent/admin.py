from django.contrib import admin
from .models import ChildName, ParentName
# Register your models here.

admin.site.register(ChildName)
admin.site.register(ParentName)